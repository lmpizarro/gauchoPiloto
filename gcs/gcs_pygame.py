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
try:
    import pygame
    import sys
    import queueInterface
    from pygame.locals import *
except ImportError, err:
    print ("%s Failed to Load Module: %s" % (__file__, err))
    import sys
    sys.exit(1)
'''
  # Define some colors
'''
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 255)
green = (0, 255,   0)
dkgreen = (0, 100, 0)
red = (255, 0, 0)
purple = (0xBF, 0x0F, 0xB5)
brown = (0x55, 0x33, 0x00)

DELAY_KEY = 4


class Proccess_Joystick:

    def __init__(self, queue):
        self.queue = queue
        pygame.joystick.init()
        self.deltaX = 0
        self.deltaY = 0

        try:  # init joystick
            self.joy = []
            self.sticks = []

            if (pygame.joystick.get_count()) == 0:
                print ("No hay joystick")

            for n in range(pygame.joystick.get_count()):
                self.stick = pygame.joystick.Joystick(n)
                self.stick.init()  # init instance
                # report joystick charateristics #
                lgstr = '-' * 20
                lgstr += '\nEnabled HID device: ' + self.stick.get_name()
                lgstr += '\nit has the following devices :'
                lgstr += '\n--> buttons : ' + str(self.stick.get_numbuttons())
                lgstr += '\n--> balls : ' + str(self.stick.get_numballs())
                lgstr += '\n--> axes : ' + str(self.stick.get_numaxes())
                lgstr += '\n--> hats : ' + str(self.stick.get_numhats())
                lgstr += '\n-' * 20
                # logging.info(lgstr)
                print (lgstr)
                self.joy.append(self.stick.get_name())
                self.sticks.append(self.stick)
        except pygame.error:
            msg = 'no HID device found??'
            print (msg)
            joy = 'False'

    def process(self, event):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""
        self.event = event

        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(30)

        msg = None

        # poll for pygame events
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:  # 7
                # JOYAXISMOTION
                msg = ['axismotion', event.joy, event.axis, event.value]
            elif event.type == JOYBALLMOTION:  # 8
                # JOYBALLMOTION
                msg = ['ballmotion', event.joy, event.ball, event.value]
            elif event.type == JOYHATMOTION:  # 9
                # JOYHATMOTION
                msg = ['hatmotion', event.joy, event.hat,
                       event.value[0], event.value[1]]
            elif event.type == JOYBUTTONDOWN:  # 10
                msg = ['button', event.joy, event.button, 1]  # JOYBUTTONDOWN
            elif event.type == JOYBUTTONUP:  # 11
                msg = ['button', event.joy, event.button, 0]  # JOYBUTTONUP
            if msg is not None:
                print ("enviado", msg)
                pass
        return True


class Proccess_Key:

    def __init__(self, queue):
        self.timeKey = 0
        self.DELAY_KEY = DELAY_KEY
        self.deltaX = 0
        self.deltaY = 0
        self.queue = queue
        pass

    def process(self, event):
        self.timeKey += 1
        self.event = event

        if self.timeKey % self.DELAY_KEY == 0:
            keyState = pygame.key.get_pressed()
            #
            # if keyState[pygame.K_UP] or keyState[pygame.K_DOWN] or
            #             keyState[pygame.K_LEFT] or keyState[pygame.K_RIGHT]:
            #   print (self.deltaX, self.deltaY)
            # elif keyState[pygame.K_KP0] or keyState[pygame.K_0]:
            #   print (self.deltaX, self.deltaY)
            #
            if keyState[pygame.K_UP]:
                self.deltaY += 1
            elif keyState[pygame.K_DOWN]:
                self.deltaY -= 1
            elif keyState[pygame.K_LEFT]:
                self.deltaX -= 1
            elif keyState[pygame.K_RIGHT]:
                self.deltaX += 1
            elif keyState[pygame.K_KP0]:
                self.deltaX = self.deltaY = 0
            elif keyState[pygame.K_0]:
                self.deltaX = self.deltaY = 0
            else:
                pass
                if self.deltaX != 0 and self.deltaX < 0:
                    self.deltaX += 1
                elif self.deltaX != 0 and self.deltaX > 0:
                    self.deltaX -= 1

                if self.deltaY != 0 and self.deltaY < 0:
                    self.deltaY += 1
                elif self.deltaY != 0 and self.deltaY > 0:
                    self.deltaY -= 1
            self.queue.mensajeToQueue = (self.deltaX, self.deltaY)


class App:

    def __init__(self, queue, control, caption="test app", width=640, height=480):
        self.width = width
        self.height = height
        self.caption = caption
        self._running = True
        self.window_surf = None
        self.size = self.width, self.height
        self.queue = queue
        self.control = control
        self.pygame = None

    def initApp(self):
        self.pygame = pygame.init()
        self.clock = pygame.time.Clock()
        self.deltaX = 0
        self.deltaY = 0
        pygame.display.set_caption(self.caption)
        self.window_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # clock for ticking
        # set the window title
        self.window_surf.fill(purple)

        self._running = True

    def getPygame(self):
        return self.pygame

    def drawBackGround(self):
        # fondo del puntero
        pygame.draw.rect(self.window_surf, green,
                         [0, 0, self.width / 3, self.width / 3], 0)
        pygame.draw.line(self.window_surf, white,
                         (self.width / 6, 0), (self.width / 6, self.width / 3))
        pygame.draw.line(self.window_surf, white,
                         (0, self.width / 6), (self.width / 3, self.width / 6))
        # base de la pantalla
        pygame.draw.rect(self.window_surf,
                         blue, [0, self.height - 40, self.width, self.height], 0)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            # if the user presses escape, quit the event loop.
            if event.key == K_ESCAPE:
                # quitting
                self._running = False
            elif event.key == K_q:
                self._running = False
            '''
            elif event.key == pygame.K_DOWN:
                self.deltaY -= 1
                print ("key down")

            elif event.key == pygame.K_UP:
                self.deltaY += 1
                print ("key UP")

            elif event.key == pygame.K_LEFT:
                self.deltaX -= 1
                print ("key LEFT")

            elif event.key == pygame.K_RIGHT:
                self.deltaX += 1
                print ("key RIGHT")
            elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                self.deltaX = self.deltaY = 0
                print ("key 0")
                '''
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            print "mouse at (%d, %d)" % (x, y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                print ("Botón izquierdo en (%d, %d)" % event.pos)
            elif pygame.mouse.get_pressed()[0] == 0:
                print ("Botón derecho en (%d, %d)" % event.pos)

    def drawPointer(self):
        x = self.width / 6
        y = self.width / 6
        pygame.draw.rect(self.window_surf, white,
                         [x - 10 + self.control.deltaX, y - 5 + self.control.deltaY, 20, 10], 0)
        pygame.draw.circle(self.window_surf, purple,
                           (x + self.control.deltaX, y + self.control.deltaY), 5)

    def drawTextBase(self):
        estado = " X: " + str(self.control.deltaX) + \
            " Y: " + str(self.control.deltaY)
        font = pygame.font.Font(None, 20)
        text = font.render(estado, 1, white)
        self.window_surf.blit(text, (10, 450))

# on_loop
    def on_loop(self):
        pass

# on_render
    def on_render(self):
        self.drawBackGround()
        self.drawPointer()
        self.drawTextBase()
        pygame.display.flip()

# on_cleanup
    def on_cleanup(self):
        print ("Bye!!")
        pygame.quit()

# on_execute
    def run(self):
        if self.initApp() is False:
            self._running = False
        '''
        # you can limit the fps by passing the desired
        # frames per seccond to tick()
        '''
        self.clock.tick(25)

        while(self._running):
            for event in pygame.event.get():
                self.control.process(None)
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

# main
if __name__ == "__main__":
    queueJ = queueInterface.QueueInterface("mensajeJ", "localhost")
    control = Proccess_Key(queueJ)
    control2 = Proccess_Joystick(queueJ)
    theApp = App(queueJ, control2, "mi app", 640, 480)
    theApp.run()
