import redis
import threading
import time

redis = redis.Redis('localhost')
toRedisOut = "estadoHMI"
fromRedisIn   = "estadoPlanta"
mensajeAutoPiloto = ""
mensajeToRedis = ""


class fromHmiToQueue ():
	def __init__ (self, queueName, sleepTime = .001):
		self.mensajeToQueue = ""
		self.queueName = queueName
		self.sendFlag = 0
		self.sleepTime = sleepTime

        def callback(self):
            while True:
                  print ("mesg", self.mensajeToRedis)
		  if self.sendFlag == 1:
                     redis.publish (self.queueName , self.mensajeToQueue)
		     self.sendFlag = 0
	          time.sleep(self.sleepTime)

        def commandToQueue(self):
            self.t = threading.Thread(target=self.callback)
            self.t.setDaemon(True)
            self.t.start()

	def sendMesagge (self, msg):
	    self.mensajeToRedis = msg
	    self.sendFlag = 1

# Envia a  la planta mensajes
#commandToRedis ()

class fromQueueToHmi():
	def __init__ (self, queueName, sleepTime = .001):
		self.mensajeQueue = ""
		self.queueName = queueName
		self.sleepTime = sleepTime

        def callback(self):
            self.sub    = redis.pubsub()
            self.sub.subscribe(self.queueName)
            while True:
	          time.sleep(self.sleepTime)
	          for m in self.sub.listen():
	              self.mensajeQueue = m["data"]
	              print "mesg from Queue: ", m

        def commandFromQueue(self):
            self.t = threading.Thread(target=self.callback)
            self.t.setDaemon(True)
            self.t.start()

        def getMessage (self):
	    return (self.mensajeQueue)	


# Lee el estado de la planta 
#commandFromRedis ()



