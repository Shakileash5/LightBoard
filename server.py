from multiprocessing import managers
import socket
import os
import sys
import multiprocessing
import threading
from contextlib import closing
import json
import random
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import utils
import room

# initialize variables
PORT_START = 1200
PORT_END = 6000
rooms = {} # list of online rooms
HOST_NAME = "127.0.0.1" # host name
PORT_NUMBER = 1200 # port number
MAX_PACKET = 32768

# TODO: interprocess communication

class Server:
    rooms = dict()
    portList = list()
    manager = None
    isRunning = False
    pipe = None
    pipe_parent = None
    pipe_child = None
    
    async def register(self, websocket):
        #self.clients.add(websocket)
        print("[+] Clients in the room ",Server.rooms)
        print(f"[+] {websocket} has joined the chat")
        await websocket.send(json.dumps({"status":"200","type": "message", "message": "Welcome to the chat!"}))
        #await self.send_all(f"{websocket} has joined the chat")
    
    async def unregister(self, websocket):
        #self.clients.remove(websocket)
        print(f"{websocket} has left the chat")
        #await self.send_all(f"{websocket} has left the chat")
    
    async def send_all(self, message):
        for client in self.clients:
            await client.send(message) 

    async def handle_message(self, websocket, message):
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        await websocket.send(json.dumps(data))
    
    def managerProcess(self):
        
        while True:
            Server.isRunning = True
            releasedPort,roomId = Server.pipe_parent.recv()
            Server.portList.insert(0,int(releasedPort))
            print(releasedPort,type(releasedPort),Server.rooms)
            del Server.rooms[int(roomId)]
            print(Server.rooms,Server.portList)
            if len(list(Server.rooms.keys())) == 0:
                Server.isRunning = False
                print("[+] Room Manager is now terminated")
                break
        return

    async def distribute(self,websocket:WebSocketServerProtocol):
        global PORT_START
        async for data in websocket:
            data = json.loads(data)
            print("[+] Message",data)
            dataDict = {}
            if int(data['type']) == 1:
                freePort,roomId = utils.roomCreationUtil(Server.rooms,HOST_NAME,PORT_START,PORT_END)
                print("[+] Free Port",freePort)
                PORT_START = freePort + 1
                if freePort == -1:
                    dataDict["status"] = 500
                    dataDict["type"] = -1
                    dataDict["message"] = "No free ports"
                else:
                    print("[+] Free port available for ",websocket ,": ",freePort)
                    dataDict["status"] = 200
                    dataDict["type"] = 1
                    dataDict["message"] = "Room created"
                    dataDict["roomId"] = roomId
                    dataDict["port"] = freePort
                    dataDict["host"] = HOST_NAME
                    if Server.manager == None or Server.isRunning == False:
                        Server.manager = threading.Thread(target=self.managerProcess)
                        Server.pipe_parent,Server.pipe_child = multiprocessing.Pipe()
                        print("pipe is ready \n\n\n",Server.pipe_parent)
                        Server.manager.start()
                        print("[+] Room Manager is now started")
                    print(Server.pipe_parent)
                    process = multiprocessing.Process(target=room.main, args=(roomId,HOST_NAME,freePort,Server.pipe_child))
                    process.start()
                    Server.rooms[roomId] = {"host":HOST_NAME,"port":freePort,"process":process}

            elif int(data['type']) == 2:
                print(Server.rooms)
                if int(data['roomId']) in Server.rooms:
                    print("[+] Room available for ",websocket ,": ",data['roomId'])
                    #Server.rooms[data['roomId']].append(websocket)
                    dataDict["status"] = 200
                    dataDict["type"] = 1
                    dataDict["message"] = "Room Available"
                    dataDict["roomId"] = int(data['roomId'])
                    dataDict["host"] = Server.rooms[int(data['roomId'])]['host']
                    dataDict["port"] = Server.rooms[int(data['roomId'])]['port']
                else:
                    print("[+] Room not available for ",websocket ,": ",data['roomId'])
                    dataDict["status"] = 400
                    dataDict["type"] = -1
                    dataDict["message"] = "Room does not exist"
            await self.sendDict(websocket, dataDict)
            print("[+] Message sent to ",websocket,": ",dataDict)
            return

    async def handle_request(self, websocket, path):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
        finally:
            await self.unregister(websocket)


if __name__ == '__main__':

    server = Server()
    start_server = websockets.serve(server.handle_request, "localhost", 8000)
    print("[+] Server Started")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    

    