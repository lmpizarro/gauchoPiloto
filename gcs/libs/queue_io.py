# -*- coding: utf-8 -*-
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

import redis

redis_server_local = "127.0.0.1"

class queue_io:
    def __init__(self, name, redis_server_, dir_=1):
        self.name = name
        self.dir_ = dir_
        if self.dir_ == 1:
            self.input_ = "input_" + name
            self.output_ = "output_" + name
        else:
            self.input_ = "output_" + name
            self.output_ = "input_" + name


        self.redis_server = redis_server_

    def __repr__(self):
        return "Nombre: " + self.name + " Subscribe: " + self.input_ +\
                " Publish: " + self.output_  

    def publish(self, m):
        redis_server.publish(self.output_, m)

redis_server = redis.Redis(redis_server_local)
redis_subscriber = redis_server.pubsub()

queues = {"console": None , "web":None, "ser":None, "udp":None}

def setup_queue (dir_=1):

    for q in queues:
        queues[q] = queue_io(q, redis_server, dir_)
    '''
    for q in queues:
        redis_subscriber.subscribe(queues[q].input_)
    '''
    print "Setup de queues_io"
    for q in queues:
        print (queues[q])


def test_():
    setup_queue ()

    while True:
        for m in redis_subscriber.listen():
            channel = m['channel']
            data = m['data']
            print channel
            if channel == "input_web":
                print "do web"
                queues["web"].publish(data)
            elif channel == "input_ser":
                print "do ser"
            elif channel == "input_udp":
                print "do udp"

