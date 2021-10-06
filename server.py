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

# initialize variables
PORT_START = 1200
PORT_END = 6000
rooms = {} # list of online rooms
HOST_NAME = "127.0.0.1" # host name
PORT_NUMBER = 1200 # port number
MAX_PACKET = 32768


class Server:
    clients = set()
    
    async def register(self, websocket):
        self.clients.add(websocket)
        print("[+] Clients in the room ",Server.clients)
        print(f"[+] {websocket} has joined the chat")
        await websocket.send("Welcome to the chat!")
        await self.send_all(f"{websocket} has joined the chat")
    
    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(f"{websocket} has left the chat")
        await self.send_all(f"{websocket} has left the chat")
    
    async def send_all(self, message):
        for client in self.clients:
            await client.send(message) 

    async def handle_message(self, websocket, message):
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def distribute(self,websocket:WebSocketServerProtocol):
        async for message in websocket:
            print("[+] Message",message)
            await self.send_all(message)

    async def handle_request(self, websocket, path):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
        finally:
            await self.unregister(websocket)


if __name__ == '__main__':

    # server = Server()
    # print("[+] Server Started")
    # start_server = websockets.serve(server.handle_request, HOST_NAME, PORT_NUMBER)
    # print("[+] Server Running")
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(start_server)
    # loop.run_forever()
    server = Server()
    start_server = websockets.serve(server.handle_request, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

    