import asyncio
import websockets
import signal
import os

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
    

start_server = websockets.serve(echo, "localhost", 8100)

asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()


  