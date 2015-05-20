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
import threading


class QueueInterface ():
    def __init__(self, channel, server, write=True):
        self.server = server
        self.mensajeToQueue = ""
        self.mensajeFromQueue = ""
        self.redis = redis.Redis(self.server)
        self.write = write
        self.channel = channel
        print ("Iniciliza cola de mensajes: ", self.write, self.channel)
        self.run()

    def publish(self):
        while True:
            if self.mensajeToQueue != "":
                #print ("Mensaje a la cola: ",self.mensajeToQueue)
                self.redis.publish(self.channel, self.mensajeToQueue)
                self.mensajeToQueue = ""
            else:
                pass

    def subscribe(self):
        self.sub = self.redis.pubsub()
        self.sub.subscribe(self.channel)
        self.mensajeFromQueue = None
        while True:
            for m in self.sub.listen():
                self.mensajeFromQueue = m["data"]
                #print "Mensaje leido: ", self.mensajeFromQueue [1:-1]

    def run(self):
        if self.write is True:
            tr = threading.Thread(target=self.publish)
            print ("publicar")
        elif self.write is False:
            tr = threading.Thread(target=self.subscribe)
            print ("subscribe")
        else:
            print ("Error creacion Queue:")

        tr.setDaemon(True)
        tr.start()
