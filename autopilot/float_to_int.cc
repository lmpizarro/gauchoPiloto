/*
* Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
*
* This file is part of gauchopiloto.
*
* gauchopiloto is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2, or (at your option)
* any later version.
*
* gauchopiloto is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with gauchoPiloto; see the file COPYING. If not, see
* <http://www.gnu.org/licenses/>.
*/
#include "float_to_int.h"
#include <stdint.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))


floatToInt16::floatToInt16 (float min_, float max_){
    minF = min_;
    maxF = max_;
    n_byteI = 2;
    uint16_t a = 1; 
    max_int = (a << (n_byteI * 8)) -1;
    p = (float) max_int /(maxF - minF);
    b = - minF * p;

}

uint16_t floatToInt16::floatToInt (float f){
  return MAX(0, MIN(f*p + b, max_int));
}


