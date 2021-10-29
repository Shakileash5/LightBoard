import json
import random
import websockets
from websockets import WebSocketServerProtocol
import asyncio
import utils
import os 
import signal
from logger import Logger

# type - 3 canvas draws
# type - 4 new member added
# type - 5 request canvas
# type - 6 canvas recieve
# type - 7 canvas update
# type - 8 member removed

# create a echo server class
class Room:
    Clients = set()
    LoggerObj = Logger.getInstance() # start the server

    def __init__(self, roomId, host, port,serverPipe):
        self.roomId = roomId
        self.host = host
        self.port = port
        self.pipe = serverPipe
        Room.LoggerObj.info(f"[+] Room {roomId} created",None,roomId)
    
    async def register(self, websocket):
        """
        Register a new client in the room.

        :param websocket: the client websocket

        return: None
        """
        Room.Clients.add(websocket)
        Room.LoggerObj.debug("[+] Clients in the room ",Room.Clients,self.roomId)
        Room.LoggerObj.info(f"[+] {websocket} has joined the room",None,self.roomId)
        await self.sendDict(websocket,json.dumps({"status":"200","type": "2", "message": "Welcome to the chat!"}))
        await self.send_all({"status":"200","type": "4", "message": f"{websocket} has joined the chat","noOfClients":len(Room.Clients)})
        #print("Okay its now joined")
        return 

    async def unregister(self, websocket):
        """
        Remove a client from the room.

        :param websocket: the client websocket

        return: None
        """
        Room.Clients.remove(websocket)
        Room.LoggerObj.info(f"{websocket} has left the chat",None,self.roomId)
        await self.send_all({"status":"200","type": "8", "message": f"{websocket} has left the chat","noOfClients":len(Room.Clients)})
        if len(Room.Clients) == 0:
            Room.LoggerObj.info("[+] No clients in the room",None,self.roomId)
            self.pipe.send((self.port,self.roomId))
            os.kill(os.getpid(), signal.SIGINT)
        return

    async def send_all(self, message,websocket=None):
        """
        Send a message to all clients in the room.

        :param message: the message to send

        return: None
        """
        for client in Room.Clients:
            if client != websocket:
                await client.send(json.dumps(message)) 
        return 
        
    async def handle_message(self, websocket, message):
        """
        Function to handle sending messages to clients.

        :param websocket: the client websocket
        :param message: the message to send

        return: Nones
        """
        await self.send_all(f"[!] {websocket} says: {message}")
    
    async def sendDict(self,websocket:WebSocketServerProtocol,data):
        """
        Send a json response to the client.

        :param websocket: the client websocket
        :param data: the data to send

        return: None
        """
        await websocket.send(json.dumps(data))
    
    async def request_canvas(self,websocket:WebSocketServerProtocol):
        """
        Request the canvas from the clients to retrieve board content to new client.

        :param websocket: the client websocket

        return: None
        """
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
        """
        Send the exsisiting canvas data to the new client.

        :param websocket: the client websocket
        :param data: the data to send

        return: None
        """
        toClient = data["forClient"]
        for client in Room.Clients:
            if str(client.id) == toClient:
                await client.send(json.dumps({"status":"200","type": "6", "message": "Sending canvas data","canvas":data["canvas"]}))
                break
        #await toClient.send(json.dumps(data))
        return

    async def distribute(self,websocket:WebSocketServerProtocol):
        """
        Handle the client requests.

        :param websocket: the client websocket

        return: None
        """
        async for data in websocket:
            data = json.loads(data)
            if data["type"] == "3":
                await self.send_all(data,websocket)
            elif data["type"] == "5":
                await self.request_canvas(websocket)
            elif data["type"] == "6":
                await self.send_canvasData(websocket,data)
            Room.LoggerObj.debug(f"[+] {websocket} sent {data}",None,self.roomId)
        return

    async def handle_request(self, websocket, path):
        """
        Handle client requests.

        :param websocket: the client websocket
        :param path: the path of the client

        return: None
        """
        await self.register(websocket)
        try:
            await self.distribute(websocket)
            #Room.LoggerObj.DEBUG("[+] Waiting for messages")
        except Exception as e:
            Room.LoggerObj.error("[-] Error",e,self.roomId)
        finally:
            await self.unregister(websocket)



def main(roomId,host, port, serverPipe):
    """
    Main function to start the server.

    :param roomId: the room id
    :param host: the host of the server
    :param port: the port of the server
    :param serverPipe: the pipe to communicate with the server

    return: None
    """
    # create a Room
    # print(serverPipe)
    room_ = Room(roomId,host,port,serverPipe)
    start_room = websockets.serve(room_.handle_request, host, port)
    asyncio.get_event_loop().run_until_complete(start_room)
    asyncio.get_event_loop().run_forever()

    return
