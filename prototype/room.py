import socket
import sys
import threading
import time
import random
import json
import os
import signal

ROOM_LIMIT = 4 # max number of clients in a room
ROOM_HOST = ('',0) # initialise room host to empty string
ROOM_CLIENTS = [] # list of clients in a room
matrix = [[0 for i in range(5)] for j in range(5)] # critical section variable to get shared


def roomManager(room_id):
    while True:
        if len(ROOM_CLIENTS) == 0:
            print(room_id,"-- Room Manager: No clients in the room --")
            print(room_id,"-- Room Manager: Closing the room --")
            os.kill(os.getpid(), signal.SIGINT)
            break
        else:
            for client in ROOM_CLIENTS:
                try:
                    client[0].send(json.dumps({"type":2,"message":"Are you Alive"}).encode())
                except:
                    print(room_id,"-- Room Manager: Client not responding --")
                    ROOM_CLIENTS.remove(client)
                    print(room_id,"-- Room Manager: Client removed --")
                    print(room_id,"-- Room Manager: ROOM_CLIENTS:",ROOM_CLIENTS)
            time.sleep(5)
    return

def handleClients(soc,conn,addr):
    while True:
        data = conn.recv(1024).decode()
        data = json.loads(data)
        print("data Recieved")
        if data['type'] == 0:
            print("-- closing this client", addr)
            conn.close()
            ROOM_CLIENTS.remove((conn, addr))
            break
        for client in ROOM_CLIENTS:
            if client[1] != addr:
                client[0].send(json.dumps(data).encode())
        print(data,addr)
        #conn.send(data.encode())
        #conn.close()  
    
    return      


def initRoom(host, port, room_id):
    print("[+] Process created for room id : ", room_id)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
    print(room_id," -- [+] Socket created")
    try:
        soc.bind((host, port)) # Bind to the port
        print(room_id," -- [+] Socket binded with : ", host, ":", port)
        soc.listen(5) # Now wait for client connection 5.
        print(room_id," -- [+] Socket listening")
        
        while True:
            conn, addr = soc.accept() # Establish connection with client.
            print(room_id," -- Got connection from", addr)
            if len(ROOM_CLIENTS) < ROOM_LIMIT:
                if len(ROOM_CLIENTS) == 0:
                    ROOM_HOST = (addr[0], addr[1])
                ROOM_CLIENTS.append((conn, addr))
                if len(ROOM_CLIENTS) == 1:
                    threading.Thread(target=roomManager, args=(room_id,)).start()
                print(room_id," -- Room clients:", len(ROOM_CLIENTS))
            print(room_id," -- ROOM_HOST:", ROOM_HOST)
            print(room_id," -- ROOM_CLIENTS:", ROOM_CLIENTS)
            threading.Thread(target=handleClients, args=(soc,conn, addr)).start()
            print("One down",ROOM_CLIENTS)
            if len(ROOM_CLIENTS) == 0:
                print(room_id,"-- Closing the Room --")
                break
    except socket.error as msg:
        print(room_id," -- Socket creation failed. Error Code : " , msg )
        sys.exit()
    soc.close()
    
    return 




