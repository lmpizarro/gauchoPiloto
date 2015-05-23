# -*- coding: utf-8 -*-
#!/usr/bin/python
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

import threading
import time
import redis
import codec_message
import comm_ports

class rt_task():

    def __init__(self, delay, ser_comm_):
        self.delay = delay
        self.next_call = time.time()
        self.ser_comm = ser_comm_

    def gen_signal(self):
        pass

    def worker(self):
        self.next_call = self.next_call + self.delay
        myTime = time.time()
        threading.Timer(self.next_call - myTime, self.worker).start()

        self.gen_signal ()

        self.ser_comm.send_message(self.mes)

class gen_mediciones(rt_task):
    pass
    def gen_signal(self):
        pass
        m4 = codec_message.encode_message(1, 3)
        num = [100, 65535, 45, 67]
        self.mes = m4.mensaje(num)


class gen_referencias (rt_task):
    pass
    def gen_signal(self):
        pass
        m3 = codec_message.encode_message(1, 4)
        num = [100, 35, 45, 67]
        self.mes = m3.mensaje(num)

def test1 ():

    ser_com = comm_ports.serial_port('#', '!', 115200, '/dev/ttyACM0')
   
    parser = codec_message.decode_message()

    tr = threading.Thread(target=ser_com.receive_mesg, args=(parser,))
    tr.setDaemon(True)
    tr.start()

    rt_gen_meas = gen_mediciones(.02, ser_com)
    rt_gen_meas.worker()

    rt_gen_refs = gen_referencias(1, ser_com)
    rt_gen_refs.worker()

    while True:
        time.sleep(10)
        m3 = codec_message.encode_message(1, 3)
        num = [100, 0, 45, 67]
        mes = m3.mensaje(num)
        ser_com.send_message(mes)


if __name__ == "__main__":
    ser_com = comm_ports.serial_port('#', '!', 115200, '/dev/ttyACM0')
    parser = codec_message.decode_message()

    while True:
         n_error = ser_com.receive_mesg(parser)
         if n_error :
             print parser.info



