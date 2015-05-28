/*
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
 * */

#ifndef DECODE_MESSAGE_H_
#define DECODE_MESSAGE_H_

#include "defs.h"

class decode_message {
    public:
        char mensaje [LONG_BUFFER_RX_GPS]; 
        uint8_t values [LONG_BUFFER_RX_GPS];
        uint16_t nums[4];
        uint8_t cks [2];
        bool error_;
        uint8_t sys_i;
        uint8_t ope_i;
        uint8_t cks_i; 
        uint8_t hex_to_int (char c);
        bool check_in_range (char c);
        void set_values ();
        bool set_nums ();
	decode_message();
    private:
};


#endif /*DECODE_MESSAGE_H_*/
