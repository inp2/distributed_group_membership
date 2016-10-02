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
        self.fail_detect = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.host,self.port))
        except (socket.error, socket.gaierror) as err_msg:
                logging.exception(err_msg)
                self.sock.close()


    def handle_join(self, msg):
        mel = {'host':msg['host'], 'port':msg['port']}

        if self.intro:
            self.mlist.add(mel, msg['time'])
            msg_init = {
                'cmd': 'init',
                'mlist': self.mlist.lst,
                'timestamps': self.mlist.timestamps
            }
            unicast(msg['host'], msg['port'], pickle.dumps(msg_init))


    def handle_leave(self, msg):
        mel = {'host':msg['host'], 'port':msg['port']}
        self.mlist.remove(mel)


    def init_faildetect(self):
        self.fail_detect = FailureDetector(self.mlist, self.host, self.port)
        self.fail_detect.run()


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
                self.init_faildetect()
            elif rcv_msg['cmd'] == 'ping':
                self.fail_detect.recv_ping(rcv_msg['data'], self.sock, addr,
                                               '%s/%d/%s' %(rcv_msg['sender_host'],
                                                            rcv_msg['sender_port'],
                                                            rcv_msg['sender_timestamp']))
