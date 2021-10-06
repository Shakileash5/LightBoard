import socket
import os
import sys
import multiprocessing
import threading
from contextlib import closing
import json
import random

# initialize variables
port_start = 1200
port_end = 6000
rooms = {} # list of online rooms
hostName = "127.0.0.1" # host name
portNumber = 1200 # port number
MAX_PACKET = 32768


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
        #data = conn.recv(1024)
        #print("[!] recieved data",data)
        #request = normalize_line_endings(recv_all(conn)) # hack again
        response = conn.recv(1024).decode()
        print(response)
        conn.sendall(b"This is working");
        i += 1
        break



    soc.close() # close the socket