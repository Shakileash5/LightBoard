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


class Server:
    rooms = dict()
    
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

    async def distribute(self,websocket:WebSocketServerProtocol):
        async for data in websocket:
            data = json.loads(data)
            print("[+] Message",data)
            dataDict = {}
            if int(data['type']) == 1:
                freePort,roomId = utils.roomCreationUtil(Server.rooms,HOST_NAME,PORT_START,PORT_END)
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
                    process = multiprocessing.Process(target=room.main, args=(roomId,HOST_NAME,freePort,))
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
    

    