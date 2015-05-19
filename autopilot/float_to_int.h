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
* along with Paparazzi; see the file COPYING. If not, see
* <http://www.gnu.org/licenses/>.
*/

#ifndef FLOAT_TO_INT_H_
#define FLOAT_TO_INT_H_

#include "defs.h"
#include <stdint.h>

class floatToInt16
{
    private:
        float minF;
        float maxF;
        uint16_t max_int;
        float p;
        float b;
        uint32_t n_byteI;
    public:
        uint16_t floatToInt (float);
        floatToInt16 (float, float);
};




#endif /*FLOAT_TO_INT_H_*/
