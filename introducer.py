#!/usr/bin/python
import sys
import logging
import random
import socket

# Returns the membership list
def create_memlist(filename):
    mems = []
    with open(filename, 'r') as my_file:
        for line in my_file:
            line = line.strip('\n')
            memb = line
            mems.append(memb)
    logging.info("Initialized Membership List: " + str(mems))
    return mems

def conn_node(memblist):
    fail_list = []
    k = 1;
    while True:
        random.shuffle(memblist)
        
        for mem in memblist:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                mess = 'ping'
                sock.settimeout(0.1)
                sock.sendto(mess, (mem,10020))
                data = ''
                try:
                    ret_buf, server_identity = sock.recvfrom(8192)
                except socket.timeout:
                    logging.info('ACK no received from node: ' + address)
            except (socket.error,socket.gaierror) as err_msg:
                logging.error('Socket Error: ' + str(err_msg))
            sock.close()

def create_clist(memblist):
    host_addr = [];
    for name in memblist:
        addr = socket.gethostbyname(name)
        host_addr.append(addr)
        logging.info(addr)
    return host_addr

def main():
    if len(sys.argv) < 2:
        print 'python introducer.py'
        sys.exit(1)
    filename = sys.argv[1]
    create_memlist(filename)
    memblist = create_memlist(filename)
    clientlist = create_clist(memblist)
    conn_node(clientlist)

if __name__ == "__main__":
    logging.basicConfig(filename = "introducerdebug.log", level=logging.INFO,filemode = "w")
    main()
