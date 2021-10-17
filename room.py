import json
import random
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import utils
import os 
import signal

# type - 3 canvas draws
# type - 4 new member added
# type - 5 request canvas
# type - 6 canvas recieve
# type - 7 canvas update
# type - 8 member removed

# create a echo server class
class Room:
    Clients = set()

    def __init__(self, roomId, host, port,serverPipe):
        self.roomId = roomId
        self.host = host
        self.port = port
        self.pipe = serverPipe
    
    async def register(self, websocket):
        Room.Clients.add(websocket)
        print("[+] Clients in the room ",Room.Clients)
        print(f"[+] {websocket} has joined the room")
        await self.sendDict(websocket,json.dumps({"status":"200","type": "2", "message": "Welcome to the chat!"}))
        await self.send_all({"status":"200","type": "4", "message": f"{websocket} has joined the chat","noOfClients":len(Room.Clients)})
        #print("Okay its now joined")
        return 

    async def unregister(self, websocket):
        Room.Clients.remove(websocket)
        print(f"{websocket} has left the chat")
        await self.send_all({"status":"200","type": "8", "message": f"{websocket} has left the chat","noOfClients":len(Room.Clients)})
        if len(Room.Clients) == 0:
            print("[+] No clients in the room")
            self.pipe.send((self.port,self.roomId))
            os.kill(os.getpid(), signal.SIGINT)
        return


    async def send_all(self, message,websocket=None):
        for client in Room.Clients:
            if client != websocket:
                await client.send(json.dumps(message)) 
        return 
        
    async def handle_message(self, websocket, message):
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        await websocket.send(json.dumps(data))
    
    async def request_canvas(self,websocket:WebSocketServerProtocol):
        flag = False
        for client in Room.Clients:
            if client != websocket:
                flag = True
                #print("sendd req",websocket.id)
                await client.send(json.dumps({"status":"200","type": "5", "message": "Requesting canvas data","forClient":str(websocket.id)}))
                break
        if not flag:
            await self.sendDict(websocket,json.dumps({"status":"200","type": "7", "message": "No canvas data available"}))
        #print("Is data available",flag)
        return 
    
    async def send_canvasData(self,websocket:WebSocketServerProtocol,data):
        toClient = data["forClient"]
        for client in Room.Clients:
            if str(client.id) == toClient:
                await client.send(json.dumps({"status":"200","type": "6", "message": "Sending canvas data","canvas":data["canvas"]}))
                break
        #await toClient.send(json.dumps(data))
        return

    async def distribute(self,websocket:WebSocketServerProtocol):
        async for data in websocket:
            data = json.loads(data)
            if data["type"] == "3":
                await self.send_all(data,websocket)
            elif data["type"] == "5":
                await self.request_canvas(websocket)
            elif data["type"] == "6":
                await self.send_canvasData(websocket,data)

            #print("[+] Message - one",data,websocket)
            #await self.sendDict(websocket,data)

    async def handle_request(self, websocket, path):
        await self.register(websocket)
        try:
            await self.distribute(websocket)
            print("[+] Waiting for messages")
        except Exception as e:
            print("[-] Error",e)
        finally:
            await self.unregister(websocket)



def main(roomId,host, port, serverPipe):
    # create a Room
    print(serverPipe)
    room_ = Room(roomId,host,port,serverPipe)
    start_room = websockets.serve(room_.handle_request, host, port)
    print("[+] Room Started at ",host,port)
    asyncio.get_event_loop().run_until_complete(start_room)
    asyncio.get_event_loop().run_forever()
