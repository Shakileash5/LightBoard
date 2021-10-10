import asyncio
import websockets
import signal
import os

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
    

def checkPort(port):
    start_server = websockets.serve(echo, "localhost", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    os.kill(os.getpid(), signal.SIGINT)
#asyncio.get_event_loop().run_forever()


  