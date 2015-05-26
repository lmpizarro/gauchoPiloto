import socket   # for sockets
import sys      # for exit
import time     # for sleep
import redis
import threading
import task_timer

class proxy_udp:
    s = None
    def __init__(self, redis_server_addr, host, port):	
	self.redis_server_addr = redis_server_addr    
        # create dgram udp socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
 
        self.host = host 
        self.port = port

        self.s.connect((self.host, self.port))

        self.redis_server = redis.Redis(self.redis_server_addr)
        self.redis_subscriber = self.redis_server.pubsub()
        self.redis_subscriber.subscribe("udp_write")

    def queue_to_udp(self):
        for m in self.redis_subscriber.listen():
            channel = m['channel']
            data =  m['data']
            if channel == "udp_write":
		print data    
                self.send_message(data)

    def write (self, m):
        self.redis_server.publish("udp_write", m)

    def send_message (self, msg):
        try :
            #Set the whole string
            self.s.send(msg)
         
            # receive data from client (data, addr)
            resp = self.s.recvfrom(1024)
            if resp == "": pass
            reply = resp[0]
            addr = resp[1]
         
            print 'Server reply : ' + reply
            self.redis_server.publish("udp_read", reply)
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def run (self):
        tr_queue_to_udp = threading.Thread(target=self.queue_to_udp, args=())
        tr_queue_to_udp.setDaemon(True)
        tr_queue_to_udp.start()
        print "proxy_udp running"

def main ():
    pu = proxy_udp("127.0.0.1", "127.0.0.1", 15550)
    pu.run()

    soh_m = task_timer.soh_mess(1, pu)
    soh_m.worker()



if __name__ == "__main__":
    main()
    while(1) :
        # msg = raw_input('Enter message to send : ')
        time.sleep (10) 

