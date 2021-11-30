#Betül Çam - BLG 433E Prject - 2021 FALL
from socket import *
from _thread import *
import threading
import time
import random
import string
import hashlib

def count_down(conn):
    global run_thread
    time_left = 30
    while time_left>=0 and run_thread:
        if run_thread == False:
            break
        if time_left % 3 == 0:
            conn.send(str(time_left).encode('utf-8'))
        time.sleep(1)
        time_left -= 1
        
PORT = 12000
privateString = "7PTXT8RNUPGZYT1II11A58XAD053AEKS\r\n"

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("", PORT))
serverSocket.listen(1)

print("The server is ready to receive.")
while True:
    conn, addr = serverSocket.accept()
    print('Connected by', addr)
    
    sentence = conn.recv(1024).decode('utf-8')
    if sentence == 'Start_Connection\r\n':
        randomString = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 32))
        conn.send(randomString.encode('utf-8'))
        
        hashed = conn.recv(40).decode('utf-8')
        if hashed == hashlib.sha1(privateString.encode('utf-8')  + randomString.encode('utf-8') ).hexdigest():
            conn.send('Authentication succesful. Do you wish to proceed?\r\n'.encode('utf-8'))
            
            message = conn.recv(5).decode('utf-8')
            if message == 'Y\r\n':
                print('Authentication is successful.')




                print('Game is started.')
                correctNumber = random.randint(0,36)
                print('Correct number is '+str(correctNumber))
                point = 0
                
                run_thread = True
                t1 = threading.Thread(target=count_down, args=(conn,))
                t1.start()
                while run_thread and t1.is_alive():
                    guess = conn.recv(40).decode('utf-8')
                    run_thread = False
                    t1.join()
                    if guess.isnumeric() == False:
                        if guess == 'even' and correctNumber % 2 ==0:
                            point += 1
                            break
                        elif guess == 'odd' and correctNumber % 2 ==1:
                            point += 1
                            break
                        else:
                            point -= 1
                            break
                    elif int(guess) == correctNumber:
                        point += 35
                        break
                    else:
                        point -= 1
                        break                    

                conn.send(str(point).encode('utf-8'))
                print('Game is ended.')
