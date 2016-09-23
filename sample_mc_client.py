import socket
import struct
import sys


# Function establishes socket, sends grep command and returns result
def send_multicast_msg(multicast_message):
    
    try:
        multicast_identity = ('224.6.45.85', 10007)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        sock.settimeout(0.1)    
        network_hop = struct.pack('b',1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, network_hop)
        sock_sent = sock.sendto(multicast_message,multicast_identity)
        ret_buf = ''
        try:
            ret_buf, server_identity = sock.recvfrom(1024) 
            print 'Received from server: %s from %s' %(ret_buf,server_identity)
        except socket.timeout:
            print 'Socket Timeout'
        
    except (socket.error,socket.gaierror) as err_msg:
        print err_msg
        
    finally:    
        sock.close()

send_multicast_msg("Test_sample")    