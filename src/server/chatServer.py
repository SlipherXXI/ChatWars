'''
Created on Apr 19, 2018

@author: rslip
'''


import socket
import sys
import select

SOCKET_LIST = []
BUFFER_SIZE = 20

def main():
    
    TCP_IP = '127.0.0.1'
    #TCP_PORT = 5005
    
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
   
    print ("Chat server started on port " + str(portNumber))
    
    while 1: 
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            if sock == serverSock: 
                clientSock, addr = serverSock.accept()
                SOCKET_LIST.append(clientSock)
                print( "Client (%s, %s) connected" % addr)
                
                broadcast(serverSock, clientSock, "%serverSock:%serverSock entered our chatting room\n" % addr)
                msg = "Connected\n"
                print(clientSock.recv(BUFFER_SIZE).decode('ascii'))
                
                clientSock.send(msg.encode('ascii'))
                
               
                
            else:
                try: 
                    # receiving data from the socket.
                    data = sock.recv(BUFFER_SIZE)
                    
                    if data:
                        #something is in the socket
                        broadcast(serverSock, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                        print(str(sock))
                        clientmsg = data.decode('ascii')
                        clientmsg = clientmsg.strip('\r\n')
                        print("Client sent:", clientmsg)
                        print('sending:',msg)
                        sock.send(msg.encode('ascii'))
                        
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            print('client exit')
                            SOCKET_LIST.remove(sock)
                                
                        # at this stage, no data means probably the connection has been broken
                        broadcast(serverSock, sock, "Client (%s, %s) is offline\n" % addr)
                        
                except:
                    broadcast(serverSock, sock, "Client (%s, %s) is offline\n" % addr)
                    continue
                
    serverSock.close()
    
# broadcast chat messages to all connected clients
def broadcast(serverSock, sock, msg):
    
    # send the message only to peer
    for socket in SOCKET_LIST:
        if socket != serverSock and socket != sock:
            try:
                socket.send(msg)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                    
if __name__=="__main__":
    
    sys.exit(main())                                  
                           
                
                