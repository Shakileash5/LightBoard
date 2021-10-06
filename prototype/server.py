import socket
import os
import sys
import multiprocessing
import threading
from contextlib import closing
import json
import random
import utils
import room

# initialize variables
port_start = 1200
port_end = 6000
rooms = {} # list of online rooms
hostName = "127.0.0.1" # host name
portNumber = 1200 # port number

def handleConnection(conn, addr):
    '''
        Handle the connection with the client.
    '''
    dataRecv = conn.recv(1024).decode() # receive data
    dataDict = {}
    try:
        dataRecv = json.loads(dataRecv) # convert to json
        print("[!] received data: ",dataRecv)
        if dataRecv["type"] == 1:
            flag = utils.roomCreationUtil(conn,rooms,hostName,port_start,port_end)
            if flag == 0:
                return
            freePort,roomId = flag
            print("[+] Free port available for ",addr,": ",freePort)
            process = multiprocessing.Process(target=room.initRoom, args=(hostName,freePort,roomId,))
            process.start()
            dataDict["roomId"] = roomId
            dataDict["status"] = 200
            dataDict["message"] = "Room created"
            dataDict["addr"] = (hostName, freePort)
            rooms[roomId] = (hostName, freePort, addr)
        elif dataRecv["type"] == 2:
            roomId = dataRecv["roomId"]
            if roomId in rooms:
                dataDict["roomId"] = roomId
                dataDict["status"] = 200
                dataDict["message"] = "Room found"
                dataDict["addr"] = (rooms[roomId][0], rooms[roomId][1])
            else:
                dataDict["status"] = 404
                dataDict["message"] = "Room not found"
        utils.sendDict(conn, dataDict)
        print("[!] sent data: ",dataDict)
    except Exception as e:
        print("[!] error: ",e)
        dataDict["status"] = 500
        dataDict["message"] = "Error"
        utils.sendDict(conn, dataDict)
        conn.close()
        return 0
    return 1

if __name__ == '__main__':

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an socket object

    print("[+] created socket")
    soc.bind((hostName, portNumber)) # bind the socket to the port number

    soc.listen(5) # listen for connections
    print("[+] listning for connection")
    i = 0
    while i<3:
        conn,addr = soc.accept() # accept the connection
        print("[!] got connection from: ",addr)
        if handleConnection(conn,addr) == 0:
            continue

        i += 1



    soc.close() # close the socket