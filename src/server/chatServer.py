'''
Created on Apr 19, 2018

@author: rslip
'''


import socket
import sys
import select
from chatProtocol import chatProtocol


def main():
    
    TCP_IP = '127.0.0.1'
    #TCP_PORT = 5005
    BUFFER_SIZE = 20
    if len(sys.argv)  != 2:
        print('Usage: python chatServer.py <port number>')
        sys.exit(1)
    
    SOCKET_LIST = []  
    
    portNumber =int(sys.argv[1])
    
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind((TCP_IP, portNumber))
    serverSock.listen(10)
    
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(serverSock)
    
    print ("Chat server started on port " + str(portNumber))
    
    while 1: 
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            if sock == serverSock: 
                clientSock, addr = serverSock.accept()
                SOCKET_LIST.append(clientSock)
                
                msg = "Connected\n"
                print(clientSock.recv(BUFFER_SIZE).decode('ascii'))
                input()
                clientSock.send(msg.encode('ascii'))
                
            else:
                try: 
                    data = sock.recv(BUFFER_SIZE)
                    
                    if data:
                        print(sock.getHostName())
                        clientmsg = data.decode('ascii')
                        clientmsg = clientmsg.strip('\r\n')
                        #print("Client sent:", clientmsg)
                        msg = kkpDict[sock].processInput(clientmsg) + "\n"
                        #print('sending:',msg)
                        sock.send(msg.encode('ascii'))
                    else:
                        if sock in SOCKET_LIST:
                            print('client exit')
                            SOCKET_LIST.remove(sock)    
                        
                except:
                    
                    continue
    serverSock.close()
                
                
                
                
                
                
                
                
                
                
                
    if __name__=="__main__":
        sys.exit(main())
        
main()
                
                
                
                
                
                
                
                
                