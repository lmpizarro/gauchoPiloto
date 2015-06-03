# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
* * Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
* *
* * This file is part of gauchopiloto.
* *
* * gauchopiloto is free software; you can redistribute it and/or modify
* * it under the terms of the GNU General Public License as published by
* * the Free Software Foundation; either version 2, or (at your option)
* * any later version.
* *
* * gauchopiloto is distributed in the hope that it will be useful,
* * but WITHOUT ANY WARRANTY; without even the implied warranty of
* * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* * GNU General Public License for more details.
* *
* * You should have received a copy of the GNU General Public License
* * along with gauchoPiloto; see the file COPYING. If not, see
* * <http://www.gnu.org/licenses/>.
'''
import socket   # for sockets
import sys      # for exit
import redis
import threading
import task_timer
from libs import packing


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
        self.q_udp_write = "udp_write" + str(self.port)
        self.q_udp_read = "udp_read" + str(self.port)

        self.s.connect((self.host, self.port))

        self.redis_server = redis.Redis(self.redis_server_addr)
        self.redis_subscriber = self.redis_server.pubsub()
        self.redis_subscriber.subscribe(self.q_udp_write)

        self.read_udp_subscriber = self.redis_server.pubsub()
        self.read_udp_subscriber.subscribe(self.q_udp_read)

    def queue_to_udp(self):
        for m in self.redis_subscriber.listen():
            channel = m['channel']
            data = m['data']
            if channel == self.q_udp_write and len(str(data)) == 24:
                #print data
                self.send_message(packing.pack_mes(str(data)))

    def write(self, m):
        self.redis_server.publish(self.q_udp_write, m)

    def read (self):
        for m in self.read_udp_subscriber.listen():
            channel = m['channel']
            data = m['data']
            if channel == self.q_udp_read:
                print data


    def send_message(self, msg):
        try:
            # Set the whole string
            self.s.send(str(msg))
            # receive data from client (data, addr)
            resp = self.s.recvfrom(1024)
            if resp == "":
                pass
            reply = resp[0]
            addr = resp[1]

            if len(str(reply)) == 24:
                reply = packing.unpack_mes(str(reply))
                #print 'Server reply : ' + reply[0]
            self.redis_server.publish(self.q_udp_read, reply[0])
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def run(self):
        tr_queue_to_udp = threading.Thread(target=self.queue_to_udp, args=())
        tr_queue_to_udp.setDaemon(True)
        tr_queue_to_udp.start()
        print "proxy_udp running"


def main():
    pu = proxy_udp("127.0.0.1", "127.0.0.1", 15550)
    pu.run()

    soh_m = task_timer.soh_mess(1, pu)
    soh_m.worker()
# if __name__ == "__main__":
#    main()
#    while(1) :
#        msg = raw_input('Enter message to send : ')
#        time.sleep (10)
