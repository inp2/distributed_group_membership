import socket
import struct
import sys

def send_multicast_msg(x):
    multicast_identity = '224.6.45.85'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    any_client = ('',10007)
    while True:
        
        try:
            sock.bind(any_client)
            my_group = socket.inet_aton(multicast_identity)
            multicast_type = struct.pack('4sL',my_group, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_type)
            buf = ''
            while True:
                buf, sender = sock.recvfrom(8192)
                print 'Received from client %s from %s' % (buf,sender)
                sock.sendto('successfull receive', sender)
        except (socket.error,socket.gaierror) as err_msg:   
            print err_msg   
     
send_multicast_msg(5)