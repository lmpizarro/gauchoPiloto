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
import queue_io
import threading

'''
ver: https://github.com/jcubic/jquery.terminal
'''
command_words = ['help', 'home', 'go','stop', 'exit', 'chau', 
                 'quit', 'mode', 'refs']

def queue_listener():
    for m in queue_io.redis_subscriber.listen():
        data = m["data"]
        channel = m["channel"]
        #print  ("channel: %s data: %s"%(channel, data))

def command_info (command):
    return  ["OK", ("command info = %s" % (command))]

def command_go (command):
    return  ["OK", "command info = %s" % (command)]

def command_help (topic):
    if topic == "go":
        str_ =  "help for go"
    elif topic == "home":
        str_ =  "help for home"
    else:
        str_ = "no implementado"
    return ["OK", str_]    

def command_refs (command_list):
    sys = int(command_list[1])
    ope = int(command_list[2])
    encode_m = codec_message.encode_message(sys,ope)
    num = [0,0,0,0]
    for i,e in enumerate(command_list[3:]):
        num[i] = int(e)

    return ["OK", encode_m.mensaje(num)]

def do_command(opts):
    origin = opts.origin
    udp_active = opts.udp_active
    serial_active = opts.serial_active
    print "debug ------------ ", origin
    while True:
        if origin == "console":
            command = raw_input("command>")
        '''    
        elif origin == "web":
            for m in queue_io.redis_subscriber.listen():
                command = m["data"]
                break;
        '''
        command_list = command.split()
        len_command = len(command_list)
        if len_command != 0:
            nombre_comando = command_list[0]
        else:
            nombre_comando = ""

        if nombre_comando in command_words:
            if nombre_comando == "exit" or nombre_comando == "chau" or\
            nombre_comando == "quit":
                sys.exit(0)

            elif nombre_comando == "refs":
                salida = command_refs (command_list)

            elif nombre_comando == "go":
                salida = command_go(nombre_comando)

            elif nombre_comando == "stop":
                salida = command_info(nombre_comando)

            elif nombre_comando == "home":
                salida = command_info(nombre_comando)

            elif nombre_comando == "help":
                if len_command == 1:
                    salida =  [("command list %s" % (command_words)), ""]
                elif len_command == 2:
                    if command_list[1] in command_words:
                        salida = [command_help (command_list[1]), ""]
                    else:
                        print [("no help for: "), command_list[1], ""]
            else:
                pass

            if origin == "console":            
                print salida[0]
            elif origin == "web":
                queue_io.queues["web"].publish(salida[0])

            # salida a udp ser proxy 
            if serial_active:
                queue_io.queues["ser"].publish(nombre_comando + ":" + salida[1])

            if udp_active:
                queue_io.queues["udp"].publish(nombre_comando + ":" + salida[1])

            print salida[1]
        else:
            pass

from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser("console.py [options]")
    parser.add_option("--origin", dest="origin",
                                  help="web or console", default="console")

    parser.add_option("--udp-active",   dest="udp_active", type="int", 
            help="udp input/output active", default=0)

    parser.add_option("--serial-active",   dest="serial_active", type="int", 
            help="serial input/output active", default=0)

    parser.add_option("--serial-port", dest="serial_port",
                                  help="serial port", default="/dev/ttyACM0")

    parser.add_option("--baudrate", dest="baudrate", type='int',
                                  help="serial port baud rate", default=115200)

    (opts, args) = parser.parse_args()

    print "opts ", (opts, args)

    if opts.origin != "console" and opts.origin != "web":
            print (("origin:  %s no implementado ")% (opts.origin.upper()))
            sys.exit(0)


    # inicia la cola de mensaje
    queue_io.setup_queue()
    queue_io.queues["web"].publish("bienvenido, client web")

    #incial el thread que escucha mensajes
    tr_listener = threading.Thread(target=queue_listener)
    tr_listener.setDaemon(True)
    tr_listener.start()

    do_command(opts)
