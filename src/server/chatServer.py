'''
Created on Apr 19, 2018

@author: rslip
'''


import socket
import sys
import select



def main():
    
    TCP_IP = '127.0.0.1'
    #TCP_PORT = 5005
    BUFFER_SIZE = 20
    if len(sys.argv)  != 2:
        print('Usage: python ChatWarsServer.py <port number>')
        sys.exit(1)
    
    SOCKET_LIST = []  
    cwpDict = {}
    
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
                
                msg = "Connected\n"
                print(clientSock.recv(BUFFER_SIZE).decode('ascii'))
                
                clientSock.send(msg.encode('ascii'))
                
                broadcast(serverSock, clientSock, "[%serverSock:%serverSock] entered our chatting room\n" % addr)
                
            else:
                try: 
                    data = sock.recv(BUFFER_SIZE)
                    
                    if data:
                        
                        print(str(sock))
                        clientmsg = data.decode('ascii')
                        clientmsg = clientmsg.strip('\r\n')
                        #print("Client sent:", clientmsg)
                        
                        #print('sending:',msg)
                        sock.send(msg.encode('ascii'))
                    else:
                        if sock in SOCKET_LIST:
                            print('client exit')
                            SOCKET_LIST.remove(sock)    
                        
                except:
                    
                    continue
                
    serverSock.close()
    
    #conn.send(msg.encode('ascii'))    
                
    if __name__=="__main__":
        sys.exit(main())
        
main()       
 
def broadcast(serverSock, sock, msg):
    SOCKET_LIST = []
    for socket in SOCKET_LIST:
        if socket != serverSock and socket != sock:
            try:
                socket.send(msg)
            except:
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                        
    
            
                
    
                
                
                
                
                
                
                
                
                