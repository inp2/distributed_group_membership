#!/usr/bin/python
import logging
import socket
import sys
import pickle
import threading


class member_list:

    def __init__(self):
        self.lst = []
        self.lock = threading.Lock()

    def add(self, addr):
        with self.lock:
            self.lst.append(addr)

    def remove(self, addr):
        with self.lock:
            self.lst.remove(addr)

    def __str__(self):
        rep =  '===== begin mlist =====\n'
        for mem in self.lst:
            rep += mem['host'] + ":" + str(mem['port']) + ":" + str(mem['time']
            rep += '\n'
        rep += '===== end mlist =====\n'
        return rep


class request_thread(threading.Thread):

    def __init__(self, sock, addr, mlist):
        super(request_thread, self).__init__()
        self.sock = sock
        self.addr = addr
        self.mlist = mlist


    def recv_msg(self):
        sock = self.sock
        while True:
            msg = sock.recv(8129)
            if msg.strip():
                if msg.find('CMD_END') != -1:
                    rcv_msg = pickle.loads(msg)
                    self.sock.close()
                    return rcv_msg

        return None


    def broadcast(self, msg):
        logging.info("Broadcast Message")
        for client in self.mlist.lst:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((client['host'], int(client['port'])))
                send_msg = pickle.dumps(msg)
                sock.send(send_msg + 'CMD_END')
                logging.info("Node Command: " + msg['cmd'])
                sock.close()
            except (socket.error, socket.gaierror) as err_msg:
                logging.exception(err_msg)
                sock.close()

    def obey(self, msg):
        if msg['cmd'] == 'join' or msg['cmd'] == 'leave':
            self.broadcast(msg)
            mel = {'host':msg['host'], 'port':msg['port'], 'time':msg['time']}
            if msg['cmd'] == 'join':
                # mel = {'host':msg['host'], 'port':msg['port']}
                self.mlist.add(mel)
                print self.mlist
                logging.info("Membership List Update: " + str(self.mlist))
            else:
                self.mlist.remove(mel)
                print self.mlist
                logging.info("Membership List Update: " + str(self.mlist))


    def run(self):
        msg = self.recv_msg()
        self.obey(msg)


def create_socket(host,port):
    intro_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intro_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        intro_socket.bind((host,port))
        logging.info("Introducer is Alive")
    except (socket.error, socket.gaierror) as err_msg:
        logging.exception(err_msg)
        intro_socket.close()
        sys.exit()
    intro_socket.listen(10);
    return intro_socket


def accept_loop(intro_socket, memlist):
    while True:
        sock, addr = intro_socket.accept()
        rt = request_thread(sock, addr, memlist)
        rt.start()


def main():
    memlist = member_list()
    host = ''
    port = 10011
    intro_socket = create_socket(host,port)
    accept_loop(intro_socket, memlist)


if __name__ == "__main__":
    logging.basicConfig(filename = "introducerdebug.log", level=logging.INFO,filemode = "w")
    main()
