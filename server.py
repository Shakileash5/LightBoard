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
from logger import Logger

# initialize variables
PORT_START = 1200
PORT_END = 6000
rooms = {} # list of online rooms
HOST_NAME = "127.0.0.1" # host name
PORT_NUMBER = 1200 # port number
MAX_PACKET = 32768

# TODO: logger and documentation

class Server:
    rooms = dict()
    portList = list(range(PORT_START,PORT_END))
    manager = None
    isRunning = False
    pipe = None
    pipe_parent = None
    pipe_child = None
    LoggerObj = Logger.getInstance() # get the logger instance
    
    @utils.exception_handler
    async def register(self, websocket):
        """
        Acknowledge a new client to the server.

        @param websocket: the client to register
        
        return: None
        """ 
        Server.LoggerObj.debug("[+] Clients in the room ",Server.rooms)
        Server.LoggerObj.info(f"[+] {websocket} has joined the chat")
        await websocket.send(json.dumps({"status":"200","type": "message", "message": "Welcome to the chat!"}))
        return 
    
    async def unregister(self, websocket):
        """
        Acknowledge a client leaving the server.

        @param websocket: the client to unregister

        return: None
        """
        #self.clients.remove(websocket)
        Server.LoggerObj.info(f"{websocket} has left the chat")
        return
    
    @utils.exception_handler
    async def send_all(self, message):
        """
        Send a message to all clients.

        @param message: the message to send

        return: None
        """
        for client in self.clients:
            await client.send(message) 
        return

    @utils.exception_handler
    async def handle_message(self, websocket, message):
        """
        Send a message to all clients.

        @param message: the message to send
        @param websocket: the client to send the message to

        return: None
        """
        await self.send_all(f"[!] {websocket} says: {message}")
        return
    
    @utils.exception_handler
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        """
        Send a json response to the client.

        @param websocket: the client to send the message to
        @param data: the data to send

        return: None
        """
        await websocket.send(json.dumps(data))
        return
    
    @utils.exception_handler
    def manage_process(self):
        """
        Manager function to manage all the rooms process, and release ports when a room is closed.
        if no room is running, the process will exit.

        return: None
        """
        while True:
            Server.isRunning = True
            releasedPort,roomId = Server.pipe_parent.recv()
            Server.portList.insert(0,int(releasedPort))
            Server.LoggerObj.debug("Check for ports",(releasedPort,type(releasedPort),Server.rooms))
            del Server.rooms[int(roomId)]
            #print(Server.rooms,Server.portList)
            if len(list(Server.rooms.keys())) == 0:
                Server.isRunning = False
                Server.LoggerObj.info("[+] Room Manager is now terminated")
                break
        return

    @utils.exception_handler
    def set_manager(self):
        """
        Set the manager for the server. if the manager is already set, it will return the manager.
        Create pipe for inter process communication between the manager and the rooms.

        return: the manager
        """
        if Server.manager == None or Server.isRunning == False:
            Server.manager = threading.Thread(target=self.manage_process) # create a new thread to manage the rooms
            Server.pipe_parent,Server.pipe_child = multiprocessing.Pipe()
            Server.manager.start() 
            Server.LoggerObj.info("[+] Room Manager is now started")
        return 

    @utils.exception_handler
    def create_room(self,websocket):
        """
        Create a new room for the client.

        @params websocket: the client to create the room for

        return: None
        """
        global PORT_START
        freePort,roomId = utils.roomCreationUtil(Server.rooms,HOST_NAME,PORT_START,PORT_END,Server.portList) # get a free port and room id not in use
        Server.LoggerObj.debug("[+] Free Port",freePort)
        dataDict = {}
        if freePort == -1: # no free port available
            dataDict["status"] = 500
            dataDict["type"] = -1
            dataDict["message"] = "No free ports"
        else: # free port available
            Server.LoggerObj.debug(f"[+] Free port available for {websocket} : {freePort}")
            dataDict["status"] = 200
            dataDict["type"] = 1
            dataDict["message"] = "Room created"
            dataDict["roomId"] = roomId
            dataDict["port"] = freePort
            dataDict["host"] = HOST_NAME
            self.set_manager() # start the manager if it is not running
            process = multiprocessing.Process(target=room.main, args=(roomId,HOST_NAME,freePort,Server.pipe_child)) # spawn a new process for the room
            process.start()
            Server.portList.pop(0)
            Server.rooms[roomId] = {"host":HOST_NAME,"port":freePort,"process":process}
        return dataDict
    
    @utils.exception_handler
    def join_room(self,websocket,data):
        """
        Join a room for the client.

        @params websocket: the client to join the room for.
        @params data: the data to join the room.

        Returns :
            dataDict: the meta data of the room.
        """
        dataDict = {}
        if int(data['roomId']) in Server.rooms: # check if the room exists
            Server.LoggerObj.info(f"[+] Room available for {websocket}: {data['roomId']}")
            #Server.rooms[data['roomId']].append(websocket)
            dataDict["status"] = 200
            dataDict["type"] = 1
            dataDict["message"] = "Room Available"
            dataDict["roomId"] = int(data['roomId'])
            dataDict["host"] = Server.rooms[int(data['roomId'])]['host']
            dataDict["port"] = Server.rooms[int(data['roomId'])]['port']
        else: # room not available
            Server.LoggerObj.error(f"[+] Room not available for {websocket} : {data['roomId']}")
            dataDict["status"] = 400
            dataDict["type"] = -1
            dataDict["message"] = "Room does not exist"
        return dataDict

    @utils.exception_handler
    async def distribute(self,websocket:WebSocketServerProtocol):
        """
        Server the clients request to join or create room.

        @params websocket: the client to join or create the room for.

        return: None
        """
        async for data in websocket:
            data = json.loads(data)
            Server.LoggerObj.debug("[+] Message",data)
            dataDict = {}
            if int(data['type']) == 1:
                dataDict = self.create_room(websocket) # create a new room

            elif int(data['type']) == 2:
                #print(Server.rooms)
                dataDict = self.join_room(websocket,data) # join an existing room

            await self.sendDict(websocket, dataDict)
            Server.LoggerObj.info(f"[+] Message sent to {websocket}: {dataDict}")
            return

    @utils.exception_handler
    async def handle_request(self, websocket, path):
        """
        Handle clients request.

        @params websocket: the client to handle the request for.
        @params path: the path of the request.

        return: None
        """
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
    

    