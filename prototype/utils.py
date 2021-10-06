import socket
import os
import sys
import json
import random

def getFirstFreePorts(host, port_start, port_end):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(" ----- Init port scanning ------ ")
    # scan for available ports
    while port_start <= port_end:
        print("Scanning port: ", port_start)
        try:
            soc.bind((host, port_start))
            port_start += 1
            soc.close()
            # return the first available port
            return port_start - 1
        except socket.error:
            port_start += 1
    
    # return no available ports
    return -1
    
def sendDict(conn,dataDict):
    dataSend = json.dumps(dataDict)
    conn.send(dataSend.encode()) # send data
    return

def roomCreationUtil(conn,rooms,hostName,port_start,port_end):
    roomId = random.randint(1000,9999)
    dataDict = {}
    while roomId in rooms:
        roomId = random.randint(1000,9999)
    freePort = getFirstFreePorts(hostName,port_start, port_end)
    if freePort == -1:
        print("[!] No free ports")
        dataDict["status"] = 500
        dataDict["message"] = "No free ports"
        sendDict(conn, dataDict)
        conn.close()
        return 0
    return freePort,roomId