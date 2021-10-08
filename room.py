import json
import random
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import utils

# create a echo server class
class Room:
    Clients = set()

    def __init__(self, roomId, host, port):
        self.roomId = roomId
        self.host = host
        self.port = port

    async def register(self, websocket):
        Room.Clients.add(websocket)
        print("[+] Clients in the room ",Room.Clients)
        print(f"[+] {websocket} has joined the room")
        await websocket.send(json.dumps({"status":"200","type": "message", "message": "Welcome to the chat!"}))
        await self.send_all(f"{websocket} has joined the chat")
    
    async def unregister(self, websocket):
        Room.Clients.remove(websocket)
        print(f"{websocket} has left the chat")
        await self.send_all(f"{websocket} has left the chat")
    
    async def send_all(self, message):
        for client in Room.Clients:
            await client.send(message) 
    
    async def handle_message(self, websocket, message):
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        await websocket.send(json.dumps(data))
    
    async def distribute(self,websocket:WebSocketServerProtocol):
        async for data in websocket:
            data = json.loads(data)
            print("[+] Message",data)
            await self.sendDict(websocket,data)

    async def handle_request(self, websocket, path):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
            print("[+] Waiting for messages")
        finally:
            await self.unregister(websocket)


# create a server
def main(roomId,host, port):
    # create a server
    room_ = Room(roomId,host,port)
    start_room = websockets.serve(room_.handle_request, host, port)
    print("[+] Room Started at ",host,port)
    asyncio.get_event_loop().run_until_complete(start_room)
    asyncio.get_event_loop().run_forever()