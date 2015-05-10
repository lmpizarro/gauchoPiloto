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

#ifndef PROTOCOL_H_
#define PROTOCOL_H_

#include "defs.h"
#include <stdint.h>

class floatToHex
{
    private:
        float minF;
        float maxF;
        uint32_t max_int;
        float p;
        float b;
        uint32_t n_byteI;
	char hexDigits [16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
    public:
	char hexs[MAX_BYTES * 2 + 1];
        floatToHex (float, float, uint32_t);
        uint32_t floatToInt (float f);
        void intToHex (uint32_t);
};




#endif /*PROTOCOL_H_*/
