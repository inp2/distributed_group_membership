#!/usr/bin/python

from memlist import *
from util import *
from failure_detector import FailureDetector


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


    def handle_join(self, msg):
        mel = {'host':msg['host'], 'port':msg['port']}
        if self.intro:
            msg_init = {
                'cmd': 'init',
                'mlist': self.mlist.lst,
                'timestamps': self.mlist.timestamps
            }
            if msg['host'] != self.host or msg['port'] != self.port:
                unicast(msg['host'], msg['port'], pickle.dumps(msg_init))
        self.mlist.add(mel, msg['time'])
        if self.intro:
            broadcast(self.mlist, self.host, self.port, pickle.dumps(msg))


    def handle_leave(self, msg):
        mel = {'host':msg['host'], 'port':msg['port']}
        self.mlist.remove(mel)


    def run(self):
        while True:
            msg, addr = self.sock.recvfrom(8129)
            rcv_msg = pickle.loads(msg)
            if rcv_msg['cmd'] == 'join' or rcv_msg['cmd'] == 'leave':
                if rcv_msg['cmd'] == 'join':
                    self.handle_join(rcv_msg)
                else:
                    self.handle_leave(rcv_msg)

                logging.info("Membership List Update: " + str(self.mlist))
            elif rcv_msg['cmd'] == 'init':
                self.mlist.init(rcv_msg['mlist'], rcv_msg['timestamps'])
                fail_detect = FailureDetector(self.mlist)
                fail_detect.run()
            elif rcv_msg['cmd'] == 'ping':
                fail_detect.recv_ping(rcv_msg['data'])
