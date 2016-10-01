#!/usr/bin/env python

from node import *

class console_client(threading.Thread):

    def __init__(self, mlist, host, port, introducer=False):
        super(console_client, self).__init__()
        self.mlist = mlist
        self.host = host
        self.port = port
        self.intro = introducer
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except (socket.error, socket.gaierror) as err_msg:
            logging.exception(err_msg)
            self.sock.close()


    def join_group(self):
        msg = {
            'cmd':'join',
            'host': self.host,
            'port': self.port,
            'time': time.time()
        }
        snd_msg = pickle.dumps(msg)
        self.sock.sendto(snd_msg + 'CMD_END', (self.mlist.ihost,self.mlist.iport))
        logging.info("Node Command: " + msg['cmd'])


    def leave_group(self):
        msg = {
            'cmd': 'leave',
            'host': self.host,
            'port': self.port
        }
        snd_msg = pickle.dumps(msg)
        broadcast(self.mlist, self.host, self.port, snd_msg)
        self.mlist.remove({'host': self.host, 'port': self.port})
        logging.info("Node Command: " + msg['cmd'])


    def run(self):
        prompt = '()==[:::::::::::::> '
        if self.intro:
            prompt = '[intro] ' + prompt
        while True:
            cmd = raw_input(prompt)
            if cmd == 'join':
                self.join_group()
            elif cmd == 'leave':
                self.leave_group()
            elif cmd == 'ls':
                print self.mlist
            elif cmd == 'li':
                if self.mlist.lst:
                    for item in self.mlist.lst:
                        if item['host'] == socket.gethostbyname(socket.gethostname()):
                            print item
                else:
                    print "ID not created until 'join'"
            elif cmd == 'exit':
                import os
                os._exit(0)
            else:
                print 'invalid command!'


if __name__ == '__main__':
    logging.basicConfig(filename="node.log", level=logging.INFO, filemode="w")
    host = socket.gethostbyname(socket.gethostname())
    port = 10012
    mlist = member_list()
    cc = console_client(mlist, host, port)
    cc.start()
    drn = drone(mlist, host, port)
    drn.start()
