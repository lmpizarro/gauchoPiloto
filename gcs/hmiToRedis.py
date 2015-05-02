# -*- coding: utf-8 -*-
__author__ = 'Administrator'
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu
'''

https://github.com/main1015/pygame-demo/blob/master/examples/move_game_controller.py
'''
import pygame
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


# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
blue     = (  50,  50, 255)
green    = (   0, 255,   0)
dkgreen  = (   0, 100,   0)
red      = ( 255,   0,   0)
purple   = (0xBF,0x0F,0xB5)
brown    = (0x55,0x33,0x00)

# Function to draw the background
def draw_background(screen):
    # Set the screen background
    screen.fill(black)

def draw_item(screen,x,y):
    pygame.draw.rect(screen,green,[0+x,0+y,30,10],0)
    pygame.draw.circle(screen,red,[15+x,5+y],7,0)

pygame.init()

screen = pygame.display.set_mode((640, 480))

# Current position
x_coord=100
y_coord=100
x_center = 85
y_center = 95
max_timon = 60
max_prof = 60

# Count the joysticks the computer has
joystick_count=pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print ("Error, I didn't find any joysticks.")
else:
    # Use joystick #0 and initialize it
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

clock = pygame.time.Clock()

done = False
while done == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
	   print ("Esto es todo amigo!!")	
           done=True

    # As long as there is a joystick
    if joystick_count != 0:

       # This gets the position of the axis on the game controller
       # It returns a number between -1.0 and +1.0
       horiz_axis_pos= my_joystick.get_axis(0)
       vert_axis_pos= my_joystick.get_axis(1)

       # Move x according to the axis. We multiply by 10 to speed up the movement.
       #x_coord=int(x_coord+horiz_axis_pos*10)
       #y_coord=int(y_coord+vert_axis_pos*10)

       x_coord=int(horiz_axis_pos*90)
       y_coord=int(vert_axis_pos*90)
       #if x_coord or y_coord != 0:
       mensajeToRedis = "#"+str(int((horiz_axis_pos + 1)* max_timon )) + "|" + str(int((vert_axis_pos + 1) * max_prof)) + "!"

    draw_background(screen)

    pygame.draw.rect(screen,purple,[0,0,200,200],0)
    pygame.draw.line(screen, white, (100, 0), (100, 200))
    pygame.draw.line(screen, white, (0, 100), (200, 100))
    # Display some text
     
    estado = ""
    pygame.draw.rect(screen,blue,[0,440,640,480],0)
    if mensajeAutoPiloto != "":
       temp = mensajeAutoPiloto[1:-1].split (',')
       estado =  " Lat: " + temp[0]  +  " Lon: " + temp[1] +  " Alt: " + temp[2]  + " CS: " + temp[3] + "g " 
    


    font = pygame.font.Font(None, 20)
    text = font.render(estado, 1, white)
    screen.blit(text, (10, 450))

    # Draw the item at the proper coordinates
    draw_item(screen,x_center + x_coord,y_center + y_coord)


    pygame.display.flip()
    clock.tick(25)

pygame.quit ()
