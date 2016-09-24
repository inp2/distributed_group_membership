import socket
import sys
import getopt
import select
import logging
import time
import random


# Function establishes socket, sends grep command and returns result
def send_ping(server_list):
    
    fail_list = []
    k = 1;
    while True:
    
        ## This could be one spot for membership list update
        random.shuffle(server_list)
        
        for address in server_list:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ping_message = 'ping'
                sock.settimeout(0.1) 
                sock_sent = sock.sendto(ping_message,(address,10020))         
                data = ''
                try:
                    ret_buf, server_identity = sock.recvfrom(8192)
                    #print 'Received ACK from server: %s from %s' %(ret_buf,server_identity)   
                except socket.timeout:
                    logging.info('ACK not received within timeout from node : ')
                    logging.info(address)
                    #fail_list.append(address)
                    ##Could server_list might not happen here ???: this might casue issues becasue server_list is outer loop control. Removing an element will shift elements by one index and we might skip sending ping to a valid node.
                    ##Fail Dissemination : Can it happen here
                    
            except (socket.error,socket.gaierror) as err_msg:
                logging.error("Socket Error")
                logging.exception(err_msg)
            finally:    
                sock.close()
        #Testing purposes, break out of loop after 20 times
        #k =k + 1
        #if (k > 20):
            #break    


def sample_clients():

    host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu', 'fa16-cs425-g01-03.cs.illinois.edu' , 'fa16-cs425-g01-04.cs.illinois.edu']
    
    #host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu']
    host_addr = [];
    local_host = socket.gethostname()
    for name in host_names: 
        if name == local_host:
            pass
        else:
            addr = socket.gethostbyname(name)
            host_addr.append(addr)
            logging.info(addr) 
    return host_addr
        
def main_sub():
    server_addr = sample_clients()
    #print server_addr
    send_ping(server_addr) 


# Main Function to connect and start logging             
if __name__ == "__main__":  
    logging.basicConfig(filename = "debugping.log", level = logging.INFO, filemode = "w")
    main_sub()
           