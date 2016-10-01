#!/usr/bin/python
import logging
import socket
import sys
import threading
import pickle
import time

class member_list:

    def __init__(self):
        self.lst = []
        self.timestamps = []
        self.lock = threading.Lock()
        self.ihost = '127.0.0.1'
        self.iport = 10011

    def init(self, lst, ts):
        with self.lock:
            self.lst = lst
            self.timestamps = ts

    def add(self, addr, timestamp):
        with self.lock:
            self.lst.append(addr)
            self.timestamps.append(timestamp)

    def remove(self, addr):
        with self.lock:
            try:
                idx = self.lst.index(addr)
                del self.lst[idx]
                del self.timestamps[idx]
            except ValueError as err:
                logging.exception(err)

    def __str__(self):
        lst = self.lst
        ts = self.timestamps
        rep =  '===== begin mlist =====\n'
        for i in range(len(self.lst)):
            rep += '%s:%s at %s\n' %(lst[i]['host'], lst[i]['port'], ts[i])
        rep += '===== end mlist =====\n'
        return rep


def broadcast(mlist, host, port, msg):
    logging.info("Broadcast Message")
    for client in mlist.lst:
        if client['host'] != host or client['port'] != port:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(msg + 'CMD_END', (client['host'], client['port']))
                logging.info('Broadcast to: %s:%d' %(client['host'], client['port']))
                sock.close()
            except (socket.error, socket.gaierror) as err_msg:
                logging.exception(err_msg)
                sock.close()


def unicast(host, port, msg):
    logging.info("Unicast Message")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg + 'CMD_END', (host, port))
        logging.info('Broadcast to: %s:%d' %(host, port))
        sock.close()
    except (socket.error, socket.gaierror) as err_msg:
        logging.exception(err_msg)
        sock.close()


class drone(threading.Thread):

    def __init__(self, mlist, host, port, introducer=False):
        super(drone, self).__init__()
        self.mlist = mlist
        self.intro = introducer
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host,self.port))
        except (socket.error, socket.gaierror) as err_msg:
                logging.exception(err_msg)
                self.sock.close()


    def run(self):
        while True:
            msg, addr = self.sock.recvfrom(8129)
            rcv_msg = pickle.loads(msg)
            if rcv_msg['cmd'] == 'join' or rcv_msg['cmd'] == 'leave':
                mel = {'host':rcv_msg['host'], 'port':rcv_msg['port']}
                if rcv_msg['cmd'] == 'join':
                    if self.intro:
                        msg_init = {
                            'cmd': 'init',
                            'mlist': self.mlist.lst,
                            'timestamps': self.mlist.timestamps
                        }
                        if rcv_msg['host'] != self.host or rcv_msg['port'] != self.port:
                            unicast(rcv_msg['host'], rcv_msg['port'], pickle.dumps(msg_init))
                    self.mlist.add(mel, rcv_msg['time'])
                    if self.intro:
                        broadcast(self.mlist, self.host, self.port, msg)
                else:
                    if self.intro:
                        broadcast(self.mlist, self.host, self.port, msg)
                    self.mlist.remove(mel)

                logging.info("Membership List Update: " + str(self.mlist))
            elif rcv_msg['cmd'] == 'init':
                self.mlist.init(rcv_msg['mlist'], rcv_msg['timestamps'])

