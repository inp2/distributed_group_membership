#!/usr/bin/env python

from node import *
from console import *


if __name__ == '__main__':
    logging.basicConfig(filename="intro.log", level=logging.INFO, filemode="w")
    host = socket.gethostbyname(socket.gethostname())
    port = 10011
    mlist = member_list()
    drn = drone(mlist, host, port, introducer=True)
    drn.start()
    cc = console_client(mlist, host, port, introducer=True)
    cc.start()
