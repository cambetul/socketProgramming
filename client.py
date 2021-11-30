#Betül Çam - BLG 433E Project - 2021 FAL
from  socket import *
from _thread import *
import threading
import hashlib
import string
import time

def print_time(conn):
    time_left = 1
    global run_thread
    while int(time_left) > 0 and run_thread:
        time_left = conn.recv(40).decode('utf-8')
        if run_thread == False:
            break
        if int(time_left) <=0:
            print('\nTIME IS UP')
            break
        else:
            print('\nREMAINING TIME: '+time_left+' seconds')

HOST = "localhost"
PORT = 12000

privateString = "7PTXT8RNUPGZYT1II11A58XAD053AEKS\r\n"

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((HOST, PORT))
except:
    print('Cannot connected to server.')
    exit(0)

clientSocket.send('Start_Connection\r\n'.encode('utf-8'))

randomString = clientSocket.recv(1024).decode('utf-8')

hashed = hashlib.sha1(privateString.encode('utf-8') + randomString.encode('utf-8')).hexdigest()
clientSocket.sendall(hashed.encode('utf-8'))

message = clientSocket.recv(1024).decode('utf-8')
if message == 'Authentication succesful. Do you wish to proceed?\r\n':
    clientSocket.send('Y\r\n'.encode('utf-8'))
    
    print('What is your guess? Number, even, odd?')
    
    run_thread = True
    t1 = threading.Thread(target=print_time, args=(clientSocket,))
    t1.start()
    
    while run_thread and t1.is_alive():
        guess = input()
        if t1.is_alive() == False:
            guess = 'wrong'
            clientSocket.sendall(guess.encode('utf-8'))
            break
        run_thread = False
        t1.join()
        clientSocket.sendall(guess.encode('utf-8'))
        break
        
    score = clientSocket.recv(40).decode('utf-8')
    print('Score: '+score)