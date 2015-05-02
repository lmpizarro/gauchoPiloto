import redis
import threading
import time

redis = redis.Redis('localhost')
toRedis = "estadoPlanta"
fromRedis   = "estadoHMI"
mensajeHMI = ""
mensajeToRedis = ""

def callbackToRedis():
    global mensajeToRedis
    while True:
          redis.publish (toRedis,mensajeToRedis)
	  time.sleep(.3)

def commandToRedis():
    tr = threading.Thread(target=callbackToRedis)
    tr.setDaemon(True)
    tr.start()

# Envia a  la planta mensajes
commandToRedis ()

def callbackFromRedis():
    global mensajeHMI
    sub    = redis.pubsub()
    sub.subscribe(fromRedis)
    while True:
	  time.sleep(.3)
	  for m in sub.listen():
	      mensajeHMI = m["data"]

def commandFromRedis():
    t = threading.Thread(target=callbackFromRedis)
    t.setDaemon(True)
    t.start()


# Lee el estado de la planta 
commandFromRedis ()

i = 0
while True:
	pass
        mensajeToRedis = "#23.1S,45.1E,456," + str(i) + "!"
	i = (i + 1.0 )%360.0
        print ("mesg estado avion: ",mensajeToRedis)
	print ("mesg estado HMI: ", mensajeHMI)
	time.sleep(.3)
