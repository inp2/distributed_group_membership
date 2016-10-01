from memlist import *

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


