#!/usr/bin/python
import logging
import socket

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
                sock.sendto('ack', sender)
        except (sock.error, socket.gaierror) as err_msg:
            print err_msg

def main():
    recv_ping()

if __name__ == "__main__":
    logging.basicConfig(filename="nodedebug.log", level=logging.INFO, filemode="w")
    main()
