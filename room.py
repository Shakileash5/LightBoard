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
        await self.sendDict(websocket,json.dumps({"status":"200","type": "2", "message": "Welcome to the chat!"}))
        await self.send_all({"status":"200","type": "4", "message": f"{websocket} has joined the chat"})
        print("Okay its now joined")
        return 

    async def unregister(self, websocket):
        Room.Clients.remove(websocket)
        print(f"{websocket} has left the chat")
        await self.send_all(f"{websocket} has left the chat")
    
    async def send_all(self, message,websocket=None):
        for client in Room.Clients:
            if client != websocket:
                await client.send(json.dumps(message)) 
        return 
        
    async def handle_message(self, websocket, message):
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        await websocket.send(json.dumps(data))
    
    async def distribute(self,websocket:WebSocketServerProtocol):
        async for data in websocket:
            data = json.loads(data)
            if data["type"] == "3":
                await self.send_all(data)
            print("[+] Message - one",data,websocket)
            #await self.sendDict(websocket,data)

    async def handle_request(self, websocket, path):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
            print("[+] Waiting for messages")
        finally:
            await self.unregister(websocket)



def main(roomId,host, port):
    # create a Room
    room_ = Room(roomId,host,port)
    start_room = websockets.serve(room_.handle_request, host, port)
    print("[+] Room Started at ",host,port)
    asyncio.get_event_loop().run_until_complete(start_room)
    asyncio.get_event_loop().run_forever()
