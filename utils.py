import socket
import os
import sys
import json
import random
import websockets
import asyncio


async def testConnection(websocket, path):
    async for message in websocket:
        await websocket.send(message)

def getFirstFreePorts(host, port_start, port_end):
    print(" ----- Init port scanning ------ ")
    # scan for available ports
    while port_start <= port_end:
        print("Scanning port: ", port_start)
        try:
            start_server = websockets.serve(testConnection, host, port_start)
            asyncio.get_event_loop().run_until_complete(start_server)
            port_start += 1
            # return the first available port
            return port_start - 1
        except socket.error:
            port_start += 1
    
    # return no available ports
    return -1

def roomCreationUtil(rooms,hostName,port_start,port_end):
    roomId = random.randint(1000,9999)
    dataDict = {}
    while roomId in rooms:
        roomId = random.randint(1000,9999)
    # TODO: check if port is available
    freePort = port_start+1 #getFirstFreePorts(hostName,port_start, port_end)
    if freePort == -1:
        print("[!] No free ports")
    return freePort,roomId