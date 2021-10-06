import socket
import sys
import json
import threading

hostName = "127.0.0.1" # server ip to get connection
portNumber = 1200 # server port to get connection

def handleCreateRoom(sock):
    dataToSend = {'type': 1}
    sock.send(str.encode(json.dumps(dataToSend)))
    dataRecved = json.loads(sock.recv(1024).decode())
    print("[*] data recieved from server : ",dataRecved)
    if dataRecved['status'] != 200:
        return 0,0,0
    roomId = dataRecved['roomId']
    hostName,port = dataRecved['addr']
    return roomId,hostName,port

def handleJoinRoom(sock,roomId):
    dataToSend = {'type': 2,'roomId':roomId}
    sock.send(str.encode(json.dumps(dataToSend)))
    dataRecved = json.loads(sock.recv(1024).decode())
    if dataRecved['status'] != 200:
        return 0,0,0
    hostName,port = dataRecved['addr']
    return roomId,hostName,port

def getConnection(hostName,portNumber):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object

    try:
        print("[*] Connecting to the server...")
        soc.connect((hostName, portNumber)) # connect to server
        print("[+] Connected to the server")
    except:
        print("[-] Connection error!")
        sys.exit()

    # get client preferences for connection
    while True:
        print("[*] Enter your preferences (1 - create room , 2 - join room, 3 - Exit) :")
        pref = int(input())
        if pref not in [1,2,3]:
            continue
        if pref == 3:
            soc.close()
            sys.exit()
        elif pref == 1:
            roomId,hostName,port = handleCreateRoom(soc) 
        elif pref == 2:
            roomId = int(input("[*] Enter room id : "))
            roomId,hostName,port = handleJoinRoom(soc,roomId) 
        if roomId == 0:
            print("[-] Cannot complete the operation")
            continue
        print("[+] data recieved from server : ",roomId,hostName,port)
        break
    soc.close()
    return roomId,hostName,port

def redirectToRoom(roomId,host,port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
    try:
        print("[*] Connecting to the server...")
        soc.connect((host, port)) # connect to server
        print("[+] Connected to the server")
    except:
        print("[-] Connection error!")
        sys.exit()
    return soc

def getData(soc):
    while True:
        dataRecved = soc.recv(1024).decode()
        if not dataRecved:
            break
        dataRecved = json.loads(dataRecved)
        if dataRecved["type"] == 2:
            continue
        print("[*] data recieved from server : ",dataRecved)
    return


def handleData(soc):
    thread = threading.Thread(target=getData, args=(soc,))
    thread.start()
    while True:
        dataToSend = input("[*] Enter data to send (q to quit) : ")
        if dataToSend == 'q':
            dataDict = {'type':0 ,'data': '-1'}
            dataDict = json.dumps(dataDict)
            soc.send(str.encode(dataDict))
            break
        dataDict = {'type':1 ,'data':dataToSend}
        dataDict = json.dumps(dataDict)
        soc.send(str.encode(dataDict))
    return

if __name__ == "__main__":
    roomId,hostName,port = getConnection(hostName,portNumber)
    if (roomId,hostName,port) == (0,0,0):
        print("[!] Error proceeding the operation")
        sys.exit()
    soc = redirectToRoom(roomId,hostName,port)
    handleData(soc)
    soc.close()