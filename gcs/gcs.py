# -*- coding: utf-8 -*-

"""
Pygame Tutorial 2 -- Setting up pygame

Collin 'Keeyai' Green
http://muagames.com
Version 1.0.0  ---  2009-11-07
License: Public Domain

http://muagames.com/tutorials/pygame-2-the-basics/

"""


try:
    import pygame, sys, os, math
    from pygame.locals import *
    import interfaQueue
except ImportError, err:
    print ("%s Failed to Load Module: %s" % (__file__, err))
    import sys
    sys.exit(1)


# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
blue     = (  50,  50, 255)
green    = (   0, 255,   0)
dkgreen  = (   0, 100,   0)
red      = ( 255,   0,   0)
purple   = (0xBF,0x0F,0xB5)
brown    = (0x55,0x33,0x00)



class GCS(object):
    """Our game object! This is a fairly simple object that handles the
    initialization of pygame and sets up our game to run."""

    def __init__(self, queue, width = 640, height = 480):
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools
        that we will need for more complicated tutorials."""

        # load and set up pygame
        pygame.init()

        self.width = width
	self.height = height
	self.queue = queue
	self.caption = 'Estación de Control'


        # create our window
        self.window = pygame.display.set_mode((self.width, self.height))
        #self.window = pygame.display.set_mode((1024, 768), FULLSCREEN)
 
        self.initScreen()

        self.initJoystick()

        # clock for ticking
        self.clock = pygame.time.Clock()

        # set the window title
        pygame.display.set_caption(self.caption)

        # tell pygame to only pay attention to certain events
        # we want to know if the user hits the X on the window, and we
        # want keys so we can close the window with the esc key
        pygame.event.set_allowed([QUIT, KEYDOWN])


    def initScreen (self):
        self.window.fill(purple)
        pygame.draw.rect(self.window, green,[0,0,self.width/3,self.width/3],0)
        pygame.draw.line(self.window, white, (self.width/6, 0), (self.width/6, self.width/3))
        pygame.draw.line(self.window, white, (0, self.width/6), (self.width/3, self.width/6))
        pygame.draw.rect(self.window, blue,[0,self.height-40,self.width, self.height],0)


    def initJoystick(self):
        try: # init joystick
            self.joy = []
            self.sticks = []
        
            pygame.joystick.init() # init main joystick device system
       
	    if (pygame.joystick.get_count()) == 0:
		   print ("No hay joystick");

            for n in range(pygame.joystick.get_count()): #
                self.stick = pygame.joystick.Joystick(n)
                self.stick.init() # init instance
                # report joystick charateristics #
                lgstr = '-'*20
                lgstr += '\nEnabled HID device: ' + self.stick.get_name()
                lgstr += '\nit has the following devices :'
                lgstr += '\n--> buttons : '+ str(self.stick.get_numbuttons())
                lgstr += '\n--> balls : '+ str(self.stick.get_numballs())
                lgstr += '\n--> axes : '+ str(self.stick.get_numaxes())
                lgstr += '\n--> hats : '+ str(self.stick.get_numhats())
                lgstr += '\n-'*20
                #logging.info(lgstr)
		print (lgstr)
            
                self.joy.append(self.stick.get_name())
                self.sticks.append(self.stick)
        except pygame.error:
            msg = 'no HID device found??'
            #logging.warning(msg)
	    print (msg)
            joy = 'False'



    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        print 'Starting Event Loop'

        running = True
        # run until something tells us to stop
        while running:

            # tick pygame clock
            # you can limit the fps by passing the desired frames per seccond to tick()
            self.clock.tick(25)

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()

            # update the title bar with our frames per second
            pygame.display.set_caption(self.caption + ' %d fps' % self.clock.get_fps())

            # render the screen, even though we don't have anything going on right now
            pygame.display.flip()

        pygame.joystick.quit()
        print 'Quitting. Thanks for playing'


    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""

     	# wait 10ms - this is arbitrary, but wait(0) still resulted
     	# in 100% cpu utilization
     	pygame.time.wait(30)

        msg = None

        # poll for pygame events
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION: # 7
                msg = [ 'axismotion', event.joy, event.axis, event.value ] # JOYAXISMOTION
            elif event.type == JOYBALLMOTION: # 8
                msg =  [ 'ballmotion', event.joy, event.ball, event.value ] # JOYBALLMOTION
            elif event.type == JOYHATMOTION: # 9
               msg =  [ 'hatmotion', event.joy, event.hat, event.value[0], event.value[1] ] # JOYHATMOTION
            elif event.type == JOYBUTTONDOWN: # 10
                msg = [ 'button', event.joy, event.button, 1 ] # JOYBUTTONDOWN
            elif event.type == JOYBUTTONUP: # 11
                msg = [ 'button', event.joy, event.button, 0 ] # JOYBUTTONUP
                
            if event.type == QUIT:
                return False

            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
		# quitting
                    return False

	    if msg is not None:
		print ("enviado", msg )
		pass
        return True


# create a gcs and run it
if __name__ == '__main__':
    queue = interfaQueue.fromHmiToQueue ("hmiState")	
    game = GCS(queue, 800, 600)
    game.run()
