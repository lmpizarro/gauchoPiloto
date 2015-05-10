/*
* Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
*
* This file is part of paparazzi.
*
* paparazzi is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2, or (at your option)
* any later version.
*
* paparazzi is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Paparazzi; see the file COPYING. If not, see
* <http://www.gnu.org/licenses/>.
*/

#include "protocol.h"
#include <stdint.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))


floatToHex::floatToHex (float min_, float max_, uint32_t n_byteI_ ){
    minF = min_;
    maxF = max_;
    n_byteI = n_byteI_;
    uint32_t a = 1; 
    max_int = (a << (n_byteI * 8)) -1;
    p = (float) max_int /(maxF - minF);
    b = - minF * p;

}

uint32_t floatToHex::floatToInt (float f){
  return MAX(0, MIN(f*p + b, max_int));
}

//
// Convierte un int a 4 char ascii 0 a F
//
void floatToHex::intToHex (uint32_t temp)
{
    uint32_t i;
    for (i=0; i < n_byteI * 2; i++){
        hexs[n_byteI * 2 - 1 - i] = hexDigits[temp & 0x000F];
        temp = temp >> 4;
    }
    hexs[i] = '\0';

}


