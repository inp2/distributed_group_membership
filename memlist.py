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
        self.ihost = socket.gethostbyname(socket.gethostname()) 
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
