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
import sys
import redis

import sys      # for exit
import time     # for sleep

import codec_message

command_words = ['help', 'home', 'go','stop', 'exit', 'chau', 
                 'quit', 'mode', 'refs']

import socket   # for sockets
class comm_udp:
    def __init__(self, port, host):
        # create dgram udp socket
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'

        self.host = host
        self.port = port

    def connect(self):
        self.udp_socket.connect((self.host, self.port))

    def send_message(self, m):
        self.udp_socket.send(m)

    # receive data from client (data, addr)
    def recv_message (self):
        self.resp = self.udp_socket.recvfrom(1024)
        if self.resp == "": 
           self.reply = "" 
           self.addr = self.reply 
        else:
           self.reply = self.resp[0] 
           self.addr = self.resp[1] 
        return self.reply

def command_info (command):
    return  ("command info = %s" % (command))

def command_go (command):
    return  ("command info = %s" % (command))

def command_help (topic):
    if topic == "go":
        str_ =  "help for go"
    elif topic == "home":
        str_ =  "help for home"
    else:
        str_ = "no implementado"
    return str_    

def command_refs (command_list):
    sys = int(command_list[1])
    ope = int(command_list[2])
    encode_m = codec_message.encode_message(sys,ope)
    num = [0,0,0,0]
    for i,e in enumerate(command_list[3:]):
        num[i] = int(e)

    return encode_m.mensaje(num)

def do_command(opts):
    origin = opts.origin

    while True:
        if origin == "console" or "udp":
            command = raw_input("command>")
        elif origin == "redis":
            for m in redis_subscriber.listen():
                command = m["data"]
                break;

        command_list = command.split()
        len_command = len(command_list)
        if len_command != 0:
            response = command_list[0]
        else:
            response = ""

        if response in command_words:
            if response == "exit" or response == "chau" or response == "quit":
                sys.exit(0)

            elif response == "refs":
                salida = command_refs (command_list)

            elif response == "go":
                salida = command_go(response)

            elif response == "stop":
                salida = command_info(response)

            elif response == "home":
                salida = command_info(response)

            elif response == "help":
                if len_command == 1:
                    salida =  ("command list %s" % (command_words))
                elif len_command == 2:
                    if command_list[1] in command_words:
                        salida = command_help (command_list[1])
                    else:
                        print ("no help for: "), command_list[1]
            if origin == "console":            
                print salida
            elif origin == "redis":
                redis_server.publish(redis_channel_publisher, salida)
            # salida a udp server    
            try :
                #Set the whole string
                udp_comm.send_message (salida)
                print udp_comm.recv_message ()
            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' +  msg[1]

        else:
            pass

'''
ver: https://github.com/jcubic/jquery.terminal
'''
server_local = "127.0.0.1"
redis_server = None
redis_subscriber = None
redis_channel_subscriber = "console_i"
redis_channel_publisher  = "console_o"

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser("console.py [options]")
    parser.add_option("--origin", dest="origin",
                                  help="queue or console", default="console")

    parser.add_option("--udp-port",   dest="udp_port", type="int", 
            help="udp output port", default=15550)

    (opts, args) = parser.parse_args()

    if not opts.origin:
        sys.exit(0)

    if opts.origin:
        if opts.origin == "redis":
            redis_server = redis.Redis(server_local)
            redis_subscriber = redis_server.pubsub()
            redis_subscriber.subscribe(redis_channel_subscriber)
            redis_server.publish(redis_channel_publisher, "bienvenido")
        elif opts.origin != "console":
            print (("origin:  %s no implementado ")% (opts.origin.upper()))
            sys.exit(0)

    udp_comm = comm_udp (opts.udp_port, server_local)
    udp_comm.connect()
    do_command(opts)
