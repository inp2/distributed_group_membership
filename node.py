#!/usr/bin/python
import logging
import socket
import sys
import cPickle as pickle
import threading
import time

def leave(host, port,tme):
    logging.info("Connecting to Introducer")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        # print time
        msg = {'cmd': 'leave', 'host': socket.gethostbyname(socket.gethostname()), 'port': '10012', 'time':tme}
        send_msg = pickle.dumps(msg)
        sock.send(send_msg + 'CMD_END')
        logging.info("Node Command: " + msg['cmd'])
        sock.close()
    except (socket.error, socket.gaierror) as err_msg:
        logging.exception(err_msg)
        sock.close()
            
def join(host, port, tme):
    logging.info("Connecting to Introducer")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        msg = {'cmd':'join', 'host': socket.gethostbyname(socket.gethostname()), 'port':'10012', 'time':tme}
        send_msg = pickle.dumps(msg)
        sock.send(send_msg + 'CMD_END')
        logging.info("Node Command: " + msg['cmd'])
        sock.close()
    except (socket.error, socket.gaierror) as err_msg:
        logging.exception(err_msg)
        sock.close()

def main():
    # host = '127.0.0.1'
    host = 'fa16-cs425-g01-01'
    port = '10011'
    tme = time.time()
    join_sig = raw_input('Enter "join":\n')
    if join_sig == 'join':
        join(host,port,tme)
    # Check for voluntary leave
    exit_sig = raw_input('Enter "exit" to voluntary leave:\n')
    if exit_sig == 'exit':
        leave(host,port,tme)

if __name__ == "__main__":
    logging.basicConfig(filename="nodedebug.log", level=logging.INFO, filemode="w")
    main()
