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
import redis

class soh_mess(task_timer.rt_task):

    def run_(self):
        pass
        msg = "#0101000F00FF0FFFFFFF99!"
	self.proxy.write(msg)

class pr_mess(task_timer.rt_task):

    def run_(self):
        pass
        msg = "#0103000F00FF0FFFFFFF99!"
	self.proxy.write(msg)



if __name__ == "__main__":
    #ps = proxy_serial.proxy_serial("127.0.0.1", "/dev/ttyACM0", 115200, '#','!')
    #ps.run()

    pu = proxy_udp.proxy_udp("127.0.0.1", "127.0.0.1", 15550)
    pu.run()

    soh_m = soh_mess(1, pu)
    soh_m.worker()

    pr_m = pr_mess(.02, pu)
    pr_m.worker()

    pu.read()

