import redis
import threading
import time

redis = redis.Redis('localhost')
toRedisOut = "estadoHMI"
fromRedisIn   = "estadoPlanta"
mensajeAutoPiloto = ""
mensajeToRedis = ""

def callbackToRedis():
    global mensajeToRedis
    while True:
          print ("mesg",mensajeToRedis)
          redis.publish (toRedisOut,mensajeToRedis)
	  time.sleep(.3)

def commandToRedis():
    tr = threading.Thread(target=callbackToRedis)
    tr.setDaemon(True)
    tr.start()

# Envia a  la planta mensajes
commandToRedis ()


def callbackFromRedis():
    global mensajeAutoPiloto
    sub    = redis.pubsub()
    sub.subscribe(fromRedisIn)
    while True:
	  time.sleep(1)
	  for m in sub.listen():
	      mensajeAutoPiloto = m["data"]
	      print "mesg estado avión: ", m

def commandFromRedis():
    t = threading.Thread(target=callbackFromRedis)
    t.setDaemon(True)
    t.start()


# Lee el estado de la planta 
commandFromRedis ()



