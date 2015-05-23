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
import math

class float_to_int16:
    def __init__(self, minf, maxf):
	self.minf = minf
	self.maxf = maxf
	self.n_byte = 2
	self.max_int = math.pow(2, 8*self.n_byte)
	self.p = self.max_int / (self.maxf - self.minf)
	self.b = - self.minf * self.p
	print self.p, self.b

    def float_to_int (self, n):
	return int ((max(0, min (n*self.p + self.b, self.max_int))))    
	 
    



'''
f_to16 = float_to_int16(-1,1)
print f_to16.float_to_int(1)
print f_to16.float_to_int(-1)
'''
