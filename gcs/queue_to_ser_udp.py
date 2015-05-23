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
from libs import comm_ports
from libs import queue_io
from libs import codec_message
import threading
import time

'''
    parser.add_option("--udp-port",   dest="udp_port", type="int", 
            help="udp output port", default=15550)

    if opts.udp_active:

     if udp_active:
        try :
             #Set the whole string
             udp_comm.send_message (salida)
             print udp_comm.receive_message ()
         except socket.error, msg:
             print 'Error Code : ' + str(msg[0]) + ' Message ' +  msg[1]

''' 

udp_server  = "127.0.0.1"
udp_comm = comm_ports.comm_udp (15550, udp_server)
udp_comm.connect()

def reroute_udp_message():
    message = udp_comm.receive_message ()
    queue_io.queues["udp"].publish(message)
    pass

# inicia la cola de mensaje en sentido inverso
queue_io.setup_queue()
queue_io.redis_subscriber.subscribe(queue_io.queues["console"].output_)

def reroute_serial_message():
    ser_com = comm_ports.serial_port('#', '!', 115200, '/dev/ttyACM0')
   
    parser = codec_message.decode_message()
    while True:
         n_error = ser_com.receive_mesg(parser)
         if n_error :
             print "ser comm: ", parser.info

             queue_io.queues["ser"].publish(parser.info)


if __name__ == "__main__":

    ser_com = comm_ports.serial_port('#', '!', 115200, '/dev/ttyACM0')

    parser = codec_message.decode_message()

    tr = threading.Thread(target=reroute_serial_message)
    tr.setDaemon(True)
    tr.start()

    while True:
        time.sleep(.01)
        for m in queue_io.redis_subscriber.listen():
            message = m["data"]
            channel = m["channel"]
            if channel == "output_console":
                print ("channel %s: %s " %(channel, message))
                ser_com.send_message(message)
                udp_comm.send_message (message)

            break;
