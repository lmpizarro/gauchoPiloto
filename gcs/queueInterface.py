# -*- coding: utf-8 -*-

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
