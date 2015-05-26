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


class soh_mess(rt_task):

    def run_(self):
        pass
        msg = "#0101000F00FF0FFFFFFF99!"
	self.proxy.write(msg)

