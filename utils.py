import socket
import os
import sys
import json
import random
import websockets
import asyncio
import multiprocessing
import sample
from logger import Logger


async def testConnection(websocket, path):
    """
    Util function to test connection with the websocket

    :param websocket: websocket object
    :param path: path

    :return: None
    """
    async for message in websocket:
        await websocket.send(message)

def getFirstFreePorts(host, port_start, port_end,rooms):
    """
    Util function to get first free port

    :param host: host name
    :param port_start: port start
    :param port_end: port end
    :param rooms: rooms

    :return: free port
    """
    #print(" ----- Init port scanning ------ ")
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

def roomCreationUtil(rooms,hostName,port_start,port_end,serverPorts):
    """
    Util function to create an room id and get free port for the room .

    :param rooms: rooms
    :param hostName: host name
    :param port_start: port start
    :param port_end: port end
    :param serverPorts: server ports

    :return: room id and  free port
    """
    roomId = random.randint(1000,9999)
    dataDict = {}
    loggerObj = Logger.getInstance()
    while roomId in rooms:
        roomId = random.randint(1000,9999)
    # TODO: check if port is available
    freePort = serverPorts[0] #getFirstFreePorts(hostName,port_start+1, port_end,rooms) #port_start+1 #
    loggerObj.debug("Free port: ", freePort)
    if freePort == -1:
        loggerObj.debug("[!] No free ports")
    return freePort,roomId

def exception_handler(func):
    """
    Decorator to handle exceptions

    :param func: function

    :return: function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            loggerObj = Logger.getInstance()
            #print("[!] Exception: ", e)
            loggerObj.error("[!] Exception: ", e)
            return None
    return wrapper