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

import sys
import codec_message

class commands():

    command_words = ['help', 'home', 'go','stop', 'exit', 'chau', 
                 'quit', 'mode', 'refs']
    salida = None

    def __init__(self, ope_):
	self.ope = ope_    
	pass    

    def stop (self, command):
        self.salida =  ["STOP", "OK", ("command info = %s" % (command))]

    def go (self, command):
        self.salida =  ["GO", "OK", "command info = %s" % (command)]

    def home (self, command):
        self.salida =  ["HOME", "OK", "command info = %s" % (command)]

    def help (self, topic):
        if topic == "go":
            str_ =  "help for go"
        elif topic == "home":
            str_ =  "help for home"
        else:
            str_ = "no implementado"
        self.salida = ["HELP", "OK", str_]    

    def refs (self, command_list):
	if len(command_list) == 7:
	    try:	
                sys = int(command_list[1])
                ope = int(command_list[2]) + self.ope
                encode_m = codec_message.encode_message(sys,ope)
                num = [0,0,0,0]
                for i,e in enumerate(command_list[3:]):
                    num[i] = int(e)
            except ValueError:
                self.salida = ["REFS", "ERROR", "NOT INTEGERS"]
		return

            self.salida = ["REFS", "OK", encode_m.mensaje(num)]
        else:
            self.salida = ["REFS", "ERROR", "LEN < 7"]

    def process (self, command):
            command_list = command.split()
            len_command = len(command_list)


            if len_command != 0:
                nombre_comando = command_list[0]
            else:
                nombre_comando = ""

            if nombre_comando in self.command_words:
                if nombre_comando == "exit" or nombre_comando == "chau" or\
                nombre_comando == "quit":
                    sys.exit(0)

                elif nombre_comando == "refs":
                    self.refs (command_list)

                elif nombre_comando == "go":
                    self.go(nombre_comando)

                elif nombre_comando == "stop":
                    self.stop(nombre_comando)

                elif nombre_comando == "home":
                    self.home(nombre_comando)

                elif nombre_comando == "help":
                    if len_command == 1:
                        self.salida  =  ["HELP", "OK",("command list %s" % (self.command_words))]
                    elif len_command == 2:
                        if command_list[1] in self.command_words:
                            self.help (command_list[1])
                        else:
                            self.salida = ["HELP", "ERROR", ("no help for: %s")% (command_list[1])]
                else:
                    self.salida = [nombre_comando, "ERROR", "no implementado"]
            else:
                self.salida = [nombre_comando, "ERROR", "comando desconocido"]
