import socket
import sys
import logging
import time
import random
import math
import threading

class FailureDetector:

    def __init__(self):
        self.buffer_recent = {}
        self.server_list = []        

    ## Function to form a piggyback packet
    def form_piggyback_packet(self,func_identifier,msg_type):
        msg_formed = msg_type    
        for key,val in  self.buffer_recent.items():
            logging.info(func_identifier + ' Reading key from dictionary ' + key)
            if val > 0:
               new_val = val - 1
               msg_formed = msg_formed + ',' + key 
               logging.info(func_identifier + ' Form package Fail/new node Information of ' + key)
               self.buffer_recent[key] = new_val
                            
        return msg_formed
    
    ## Function to update the recently received buffer list
    def update_buffer_list(self,func_identifier, address_id_list):
        size = len(self.server_list)        
        dissemination_cnt = int(math.ceil((math.log(size,2))))     
        for address_id in address_id_list:
            logging.info(func_identifier + ' Check Recent Buffer for ' + address_id)
            if address_id not in self.buffer_recent:
                self.buffer_recent[address_id] = dissemination_cnt
                logging.info(func_identifier + ' Write to dictionary key ' + address_id +  ' value ' + str(dissemination_cnt) )
    
  ###Dummy function until Imani integrates

    def update_server_list(self):
       
       for key,val in self.buffer_recent.items():
           addr = key.split('_')
           
           #01_failaddressid, 01_nodeleaveid
           #Remove the fail address if it exists in membership list    
           if addr[0] == '01':
               if addr[1] in self.server_list:
                   self.server_list.remove(addr[1]);
                   logging.info('Update membership list with removal of' + addr[1])
           #10_newnodeid, Add the new node if it is not in membership list already
           elif addr[0] == '10':
               size = len(self.server_list) 
               insert_location = random.random() % size
               if addr[1] not in self.server_list:
                   self.server_list.insert(insert_location, addr[1])
                   logging.info('Update membership list with addition of' + addr[1])
           ##Garbage collection for buffer_recent
           if val == 0:
               self.buffer_recent.pop(key)
           
    def send_ping(self,lock):
        while True:                
            random.shuffle(self.server_list)    
            lock.acquire()
            self.update_server_list()
            lock.release() 
            for address in self.server_list:
                fail_indicator = False 
                fail_address = '01_' + address
                ## Do not send pings to already fail node 
                lock.acquire()
                if fail_address in self.buffer_recent:
                    fail_indicator = True
                lock.release()
                if fail_indicator == True:
                    continue  
                      
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(0.120) 
                    lock.acquire()                
                    ping_message = self.form_piggyback_packet('send_ping', 'p') 
                    lock.release()                                 
                    sock_sent = sock.sendto(ping_message,(address,10020))         
                    data = ''
                    try:                                            
                        ret_buf, server_identity = sock.recvfrom(8192)
                        #print 'Received ACK from server: %s from %s' %(ret_buf,server_identity)   
                    except socket.timeout:
                        logging.info('ACK not received within timeout from node : ' + address)
                        address_id = []
                        address_id.append('01_' + address)
                        lock.acquire() 
                        #logging.info('Update recent buffer from send_ping')                   
                        self.update_buffer_list('send_ping', address_id)      
                        lock.release()                    
                except (socket.error,socket.gaierror) as err_msg:
                    logging.error("Socket Error")
                    logging.exception(err_msg)
                finally:    
                    sock.close()            


    def recv_ping(self,lock):  
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        any_client = ('',10020)
        
        while True:        
            try:
                sock.bind(any_client)            
                buf = ''
                ack_message = 'a'
                while True:
                    buf, sender = sock.recvfrom(8192)
                    lock.acquire()
                    ack_message = self.form_piggyback_packet('recv_ping', 'a')  
                    lock.release()                
                    sock.sendto(ack_message, sender)
                    data = buf.split(',')    
                    lock.acquire() 
                    self.update_buffer_list('recv_ping', data[1:len(data)-1]) 
                    lock.release()                
            except (socket.error,socket.gaierror) as err_msg:   
                logging.exception(err_msg) 

### Dummy function until Imani integrates
    def sample_clients(self):
        host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu', 'fa16-cs425-g01-03.cs.illinois.edu' , 'fa16-cs425-g01-04.cs.illinois.edu', 'fa16-cs425-g01-05.cs.illinois.edu', 'fa16-cs425-g01-06.cs.illinois.edu', 'fa16-cs425-g01-07.cs.illinois.edu', 'fa16-cs425-g01-08.cs.illinois.edu']
        
        #host_names = [ 'fa16-cs425-g01-01.cs.illinois.edu', 'fa16-cs425-g01-02.cs.illinois.edu']
        host_addr = [];
        local_host = socket.gethostname()
        for name in host_names: 
            if name == local_host:
                pass
            else:
                addr = socket.gethostbyname(name)
                self.server_list.append(addr)
                logging.info(addr) 
    
        
    def run(self):
        self.sample_clients() 
        try:  
            lock = threading.Lock()    
            recv_thread = threading.Thread(target=self.recv_ping,args=(lock,))
            recv_thread.daemon = True
            recv_thread.start()     
            time.sleep(60)    
            ping_thread = threading.Thread(target=self.send_ping,args=(lock,))
            ping_thread.daemon = True
            ping_thread.start() 
            print("All threads started")
            while True:
                time.sleep(1)
        except(KeyboardInterrupt, SystemExit):
            print("exiting all threads and main program")
            
# Main Function to connect and start logging             
if __name__ == "__main__": 
    FORMAT = '%(asctime)-15s  %(message)s'
    logging.basicConfig(format = FORMAT, filename = "faildetector.log", level = logging.INFO, filemode = "w")
    fail_detect = FailureDetector()
    fail_detect.run()
           