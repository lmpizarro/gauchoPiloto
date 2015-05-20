#!/usr/bin/env python
#This script requires the following Python modules:
#  pygame   - http://www.pygame.org/
#
# source: https://github.com/gourneau/Python-RTW/blob/master/drivedata.py
#
import sys
import optparse
import logging
import simplejson

import sys
import pygame

from pygame.locals import *

# allow multiple joysticks
joy = []

# handle joystick event
def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"

        if (e.dict['axis'] == 1):
            axis = "Y"

        if (e.dict['axis'] == 2):
            axis = "Z"

        if (e.dict['axis'] == 3):
            axis = "W" 

        if (axis != "unknown"):
	    str = {'event': 'axis', 'val': e.dict['value'],  'Axis': axis}

    elif e.type == pygame.JOYHATMOTION:
        str = {'event': 'hat', 'val':  e.dict['value']}

    elif e.type == pygame.JOYBUTTONDOWN:
        str = {'event': 'button', 'val': e.dict['button']}
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 0):
            quit()
    print (str)
    
# wait for joystick input
def joystickControl():
    while True:
	try: 
            # JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
	    e = pygame.event.wait()
	    if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN\
				or e.type == pygame.JOYHATMOTION):
		handleJoyEvent(e)
	except KeyboardInterrupt:
            print "\nGot keyboard interrupt. Exiting..."
	    sys.exit(0)

# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print "\nI could not find a joystick, please plug one in, or un-plug and re-plug back in your current joystick.\n"
        quit()
    print "\n%d joystick detected." % pygame.joystick.get_count()
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print "Joystick %d: " % (i) + joy[i].get_name()
    print "Pull trigger (button 0) to quit.\n"
    # run joystick listener loop
    joystickControl()
    
# allow use as a module or standalone script
if __name__ == "__main__":
    main()

