import socket
import os
import sys
import json
import random
import websockets
import asyncio
import multiprocessing
import sample


async def testConnection(websocket, path):
    async for message in websocket:
        await websocket.send(message)

def getFirstFreePorts(host, port_start, port_end,rooms):
    print(" ----- Init port scanning ------ ")
    # scan for available ports
    while port_start <= port_end:
        if port_start not in rooms.keys():
            print("Port: ", port_start)
            return port_start
        else:
            port_start += 1
        # print("Scanning port: ", port_start)
        # try:
        #     process = multiprocessing.Process(target=sample.checkPort, args=(port_start,))
        #     process.start()
        #     port_start += 1
        #     # return the first available port
        #     return port_start - 1
        # except socket.error:
        #     print("Port not available")
        #     port_start += 1
    
    # return no available ports
    return -1

def roomCreationUtil(rooms,hostName,port_start,port_end):
    roomId = random.randint(1000,9999)
    dataDict = {}
    while roomId in rooms:
        roomId = random.randint(1000,9999)
    # TODO: check if port is available
    freePort = getFirstFreePorts(hostName,port_start+1, port_end,rooms) #port_start+1 #
    print("Free port: ", freePort)
    if freePort == -1:
        print("[!] No free ports")
    return freePort,roomId