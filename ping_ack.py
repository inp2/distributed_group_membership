import socket
import sys
import getopt
import select
import logging
import time


# Function establishes socket, sends grep command and returns result
def send_ping(server_list):

    for address in server_list:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ping_message = 'ping'
            sock.settimeout(0.1) 
            sock_sent = sock.sendto(ping_message,(address,10020))         
            data = ''
            try:
                ret_buf, server_identity = sock.recvfrom(8192)
                print 'Received ACK from server: %s from %s' %(ret_buf,server_identity)   
            except socket.timeout:
                print 'Timeout occured'
            
        except (socket.error,socket.gaierror) as err_msg:
            print err_msg
    
        finally:    
            sock.close()



def sample_clients():

    host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu', 'fa16-cs425-g01-03.cs.illinois.edu' , 'fa16-cs425-g01-03.cs.illinois.edu']
    
    #host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu']
    host_addr = [];
    local_host = socket.gethostname()
    for name in host_names: 
        if name == local_host:
            pass
        else:
            host_addr.append(socket.gethostbyname(name))
  
    return host_addr
        
def main_sub():
    server_addr = sample_clients()
    print server_addr
    send_ping(server_addr) 

main_sub()           