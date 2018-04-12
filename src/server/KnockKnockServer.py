'''
Created on Feb 12, 2018

@author: rslip
http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
'''
import socket
import sys
import select
from KnockKnockProtocol import KnockKnockProtocol
from symbol import except_clause



def main():
    kkp = KnockKnockProtocol()
    TCP_IP = '127.0.0.1'
    #TCP_PORT = 5005
    BUFFER_SIZE = 20
    if len(sys.argv)  != 2:
        print('Usage: python KnockKnockServer.py <port number>')
        sys.exit(1)
    
    SOCKET_LIST = []  
    kkpDict = {}
    #input('>')
    
    portNumber = int(sys.argv[1])
    #print(portNumber)
    
    #try:
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
                kkpDict[clientSock] = KnockKnockProtocol() #process a sent and returned msg
                #print(clientSock)
                #print( "Client (%serverSock, %serverSock) connected" % addr)
                #msg = kkpDict[clientSock].processInput('') + '\n'
                msg = "Connected\n"
                input()
                clientSock.send(msg.encode('ascii'))
                 
                #broadcast(server_socket, clientSock, "[%serverSock:%serverSock] entered our chatting room\n" % addr)
            else:
                try: 
                    data = sock.recv(BUFFER_SIZE)
                    
                    if data:
                        
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
    ''' 
    def broadcast(serverSock, sock, msg):
        for socket in SOCKET_LIST:
            if socket != serverSock and socket != sock:
                try:
                    socket.send(msg)
                except:
                    socket.close()
                    if socket in SOCKET_LIST:
                        SOCKET_LIST.remove(socket)
           
    conn, addr = serverSock.accept()
    print( 'Connection address:', addr)
    '''
        
    
    kpp = KnockKnockProtocol()
    msg = kkp.processInput('') + "\n"
    #print('sending:',msg)
    conn.send(msg.encode('ascii')) 
    '''
    while 1:
        # step 1, recieve data
        data = conn.recv(BUFFER_SIZE)
        if not data: break 
        clientmsg = data.decode('ascii')
        clientmsg = clientmsg.strip('\r\n')
        #print('recieved:',clientmsg)
        
        #step 2
        msg = kkp.processInput(clientmsg) + "\n"
        #print('sending:',msg)
        
        #step 3
        conn.send(msg.encode('ascii'))
        '''
          
    #except Exception as exception:
        #print(exception)
        #print("connection closed unepectedly")
    if __name__=="__main__":
        sys.exit(main())        
        
       
       
main()