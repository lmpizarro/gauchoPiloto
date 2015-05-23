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


from sets import Set


class decode_message:
    hexaChars = Set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                     'B', 'C', 'D', 'E', 'F', '#', '!'])

    info = None

    def __init__(self):
        pass

    def message_is_hexa(self, message):
        condition = True
        for e in message:
            condition = condition and (e in self.hexaChars)
        return condition

    def _4hexa_to_byte(self, s):
        return int(s[3], 16) + 16 * int(s[2], 16) + 16 * 16 * int(s[1], 16) +\
            16 * 16 * 16 * int(s[0], 16)

    def _2hexa_to_byte(self, s):
        return int(s[1], 16) + 16 * int(s[0], 16)

    def parse_message(self, message):
        self.nums = []
        mensaje = message.upper()
        len_mensaje = len(mensaje)
        if (self.message_is_hexa(mensaje) and len_mensaje >= 22):
            self.sys = mensaje[0:2]
            self.ope = mensaje[2:4]
            error = 0
        else:
            error = 1
        if error == 0:
            self.sys_i = self._2hexa_to_byte(self.sys)
            self.ope_i = self._2hexa_to_byte(self.ope)
            self.nums.append(self._4hexa_to_byte(mensaje[4:8]))
            self.nums.append(self._4hexa_to_byte(mensaje[8:12]))
            self.nums.append(self._4hexa_to_byte(mensaje[12:16]))
            self.nums.append(self._4hexa_to_byte(mensaje[16:20]))
            self.info = {'sys': self.sys_i, 'ope': self.ope_i, 'nums': self.nums}
            #print info

        return error    


class encode_message:

    def __init__(self, sys_, ope_):
        self.sys = sys_
        self.ope = ope_
        pass

    def mensaje(self, num):
        self.num = num
        mensaje = "#" + hex(self.sys)[2:].zfill(2) + hex(self.ope)[2:].zfill(2)
        sum_num = self.sys + self.ope
        for n in self.num:
            if n > 65535:
                n = 65535
            elif n < 0:
                n = 0

            sum_num += n
            mensaje += hex(n)[2:].zfill(4)
        hex_sum_num = hex(sum_num)[2:].zfill(4)
        len_hex_sum_num = len(hex_sum_num)
        cks = hex_sum_num[len_hex_sum_num - 2:]
        mensaje = mensaje + cks + '!'
        return mensaje.upper()


