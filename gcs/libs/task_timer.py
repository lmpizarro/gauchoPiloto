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
MESSAGE_REFS = 2 

import threading
import sys      # for exit
import time     # for sleep

class rt_task():
    def __init__(self, delay, proxy):
        self.next_call = time.time()
        self.delay = delay
        self.next_call = self.next_call + self.delay
        self.proxy = proxy

    def run_(self):
        pass

    def worker(self):
        self.next_call = self.next_call + self.delay
        myTime = time.time()
        threading.Timer(self.next_call - myTime, self.worker).start()

        self.run_ ()



