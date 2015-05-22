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

import socket   # for sockets
import serial

class comm_udp:
    def __init__(self, port, host):
        # create dgram udp socket
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'

        self.host = host
        self.port = port

    def connect(self):
        try:
            self.udp_socket.connect((self.host, self.port))
        except socket.error:
            print 'Failed to connect socket'

    def send_message(self, m):
        try:
            self.udp_socket.send(m)
        except socket.error:
            print 'Failed to send_message'

    # receive data from client (data, addr)
    def recv_message (self):
        self.resp = self.udp_socket.recvfrom(1024)
        if self.resp == "": 
           self.reply = "" 
           self.addr = self.reply 
        else:
           self.reply = self.resp[0] 
           self.addr = self.resp[1] 
        return self.reply



class serial_port:
    def __init__(self, start, end, speed, port_):
        self.start_ = start
        self.end_ = end
        self.flag_start = 0
        self.serial_comm = serial.Serial(
            port=port_,
            baudrate=speed,
            timeout=None,
        )

    def receive_mesg(self, parser):
        self.mensaje = ""
        while True:
            while self.serial_comm.inWaiting() > 0:
                c = self.serial_comm.read(1)
                if c == self.start_:
                    self.flag_start = 1
                    self.mensaje = ""
                elif c != self.end_ and self.flag_start == 1:
                    self.mensaje += c
                elif c == self.end_ and self.flag_start == 1:
                    parser.parse_message(self.mensaje)
                    self.mensaje = ""
                    return True

    def send_message(self, m):
        self.serial_comm.write(m)

