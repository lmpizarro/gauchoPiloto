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
from libs import proxy_serial
from libs import proxy_udp
from libs import task_timer
from libs import float_to_int
from libs import codec_message
from libs import message_defs

import redis


class soh_mess(task_timer.rt_task):

    def run_(self):
        pass
        msg = "#0101000F00FF0FFFFFFF99!"
        self.proxy.write(msg)


class pr_mess(task_timer.rt_task):
    address = 1
    mess_def_example = message_defs.MENSAJE_EXAMPLES
    st_f = [0.5, 2.0, 1.2, 3.0]
    st_i = [0,0,0,0]

    encode = codec_message.encode_message(address, mess_def_example)

    f_to16_f10 = float_to_int.float_to_int16(-1, 1)
    f_to16_f11 = float_to_int.float_to_int16(-1, 2)
    f_to16_f12 = float_to_int.float_to_int16(-0, 4)
    f_to16_f13 = float_to_int.float_to_int16(-5, 5)

    f_to_16 = [f_to16_f10, f_to16_f11, f_to16_f12, f_to16_f13]

    def encode_nums_example(self):
        self.st_i = []
        for n, f in zip(self.st_f, self.f_to_16):
            self.st_i.append(f.float_to_int(n))
        return self.encode.mensaje(self.st_i)   

    def run_(self):
        pass
        msg = self.encode_nums_example()
        self.proxy.write(msg)


if __name__ == "__main__":
    # ps = proxy_serial.proxy_serial("127.0.0.1", "/dev/ttyACM0", 115200, '#','!')
    # ps.run()

    pu = proxy_udp.proxy_udp("127.0.0.1", "127.0.0.1", 15550)
    pu.run()

    soh_m = soh_mess(1, pu)
    soh_m.worker()

    pr_m = pr_mess(.02, pu)
    pr_m.worker()

    pu.read()
