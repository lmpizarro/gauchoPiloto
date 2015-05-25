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

from optparse import OptionParser
import threading
from libs import queue_io
from libs import commands



'''
ver: https://github.com/jcubic/jquery.terminal
'''

# inicia la cola de mensaje
queue_io.setup_queue()
queue_io.redis_subscriber.subscribe(queue_io.queues["ser"].output_)
def queue_listener():
    for m in queue_io.redis_subscriber.listen():
        data = m["data"]
        channel = m["channel"]
        print  ("channel: %s data: %s"%(channel, data))


if __name__ == "__main__":
    parser = OptionParser("console.py [options]")

    parser.add_option("--udp-active",   dest="udp_active", type="int", 
            help="udp input/output active", default=0)

    parser.add_option("--serial-active",   dest="serial_active", type="int", 
            help="serial input/output active", default=0)


    (opts, args) = parser.parse_args()

    print "opts ", (opts, args)



    #incial el thread que escucha mensajes
    tr_listener = threading.Thread(target=queue_listener)
    tr_listener.setDaemon(True)
    tr_listener.start()

    prcs_command = commands.commands()

    while True:
        command = raw_input("command>")
	prcs_command.process(command) 
        print prcs_command.salida
        # salida a udp ser proxy 
        queue_io.queues["console"].publish(prcs_command.salida)

