'''
Created on Apr 19, 2018
@author: rslip
'''


import socket
import sys
import select


class User():
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        



TCP_IP = '127.0.0.1'
    #TCP_PORT = 5005
SOCKET_LIST = []
BUFFER_SIZE = 20
socketToUser={}
password = "mypassword"

def main():
    
    if len(sys.argv)  != 2:
        print('Usage: python ChatWarsServer.py <port number>')
        sys.exit(1)
        
    portNumber = int(sys.argv[1])
    
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind((TCP_IP, portNumber))
    serverSock.listen(10)
    print('server started')
    
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(serverSock)
   
    while 1: 
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            if sock == serverSock: 
                clientSock, addr = serverSock.accept()
                SOCKET_LIST.append(clientSock)
                print( "Client (%s, %s) connected" % addr)
                clientSock.send(chat_encode("Welcome to Chat Wars"))
                clientSock.send(chat_encode("please enter user name"))
                clientSock.send(chat_encode("Enter password"))
                
                data = clientSock.recv(BUFFER_SIZE)
                clientmsg= chat_decode(data)
                
                ip, port = clientSock.getpeername()
                socketToUser[clientSock] = User(clientmsg , ip , port)
                broadcast(serverSock, clientSock, "entered our chat room")
                
            else:
                try: 
                    # receiving data from the socket.
                    data = sock.recv(BUFFER_SIZE)
                    
                    if data:
                        #something is in the socket
                        clientmsg = chat_decode(data)
                        broadcast(serverSock, sock, clientmsg)
                        print(str(sock))
                        print("Client sent:", clientmsg)
                        
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            print('client exit')
                            SOCKET_LIST.remove(sock)
                                
                        # at this stage, no data means probably the connection has been broken
                        broadcast(serverSock, sock, " is offline" )
                        
                except Exception as inst:
                    print(inst)
                    #broadcast(serverSock, sock, "Client (%s, %s) is offline" % addr)
                    continue
                
    serverSock.close()
    
# broadcast chat messages to all connected clients
def broadcast(serverSock, sock, msg):
    
    # send the message only to peer
    for socket in SOCKET_LIST:
        if socket != serverSock and socket != sock:
            try:
                user = socketToUser[sock]
                socket.send(chat_encode('[' + user.name + ']' + msg))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                    
def chat_encode(msg):
    temp = msg + '\n'
    return temp.encode('ascii')

def chat_decode(msg):
    temp = msg.decode('ascii')
    return temp.strip('\r\n')
    
if __name__=="__main__":
    
    sys.exit(main())                                  
                           
                
                