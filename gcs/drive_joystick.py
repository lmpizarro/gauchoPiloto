# -*- coding: utf-8 -*-
#/usr/bin/python
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

import float_to_int
import codec_message

# allow multiple joysticks
joy = []

f_to16 = float_to_int.float_to_int16(-1,1)
nums_joys = [32768, 32768, 32768, 32768]
nums_buttons = [0, 0, 0, 0]
sys_e = 1
enc_msg = codec_message.encode_message(sys_e)

TYPE_AXIS = 10
TYPE_BUTTON = 20

# handle joystick event
def handleJoyEvent(e):
    str = ""
    type_e = 0
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = 0 

        if (e.dict['axis'] == 1):
            axis = 1 

        if (e.dict['axis'] == 2):
            axis = 2 

        if (e.dict['axis'] == 3):
            axis = 3 

        if (axis != "unknown"):
	    #str = {'event': 'axis', 'val': f_to16.float_to_int(e.dict['value']),  'Axis': axis}
	    nums_joys[axis] = f_to16.float_to_int(e.dict['value'])
	    type_e = TYPE_AXIS

        print enc_msg.mensaje(nums_joys, type_e)
    elif e.type == pygame.JOYHATMOTION:
        str = {'event': 'hat', 'val':  e.dict['value']}
	nums_buttons[1] = e.dict['value'][0] + 2
	nums_buttons[2] = e.dict['value'][1] + 2
	type_e = TYPE_BUTTON
	print enc_msg.mensaje(nums_buttons, type_e)

    elif e.type == pygame.JOYBUTTONDOWN:
        str = {'event': 'button', 'val': e.dict['button']}
	type_e = TYPE_BUTTON
	if nums_buttons[0] == e.dict['button']:
           nums_buttons[0] = 0
        else:   
	   nums_buttons[0] = e.dict['button']

	print enc_msg.mensaje(nums_buttons, type_e)
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 0):
            quit()
    #print (str)
    
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

