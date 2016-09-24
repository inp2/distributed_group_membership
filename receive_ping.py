import socket
import sys
import getopt
import select
import logging
import time

def recv_ping():  
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    any_client = ('',10020)  
    while True:
        
        try:
            sock.bind(any_client)            
            buf = ''
            while True:
                buf, sender = sock.recvfrom(8192)
                print 'Received from client %s from %s' % (buf,sender)
                sock.sendto('ack', sender)
        except (socket.error,socket.gaierror) as err_msg:   
            print err_msg 

recv_ping()