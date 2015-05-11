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

#include "pid.h"

PID::PID (float k_p_, float k_d_, float k_i_){
    k_p = k_p_;
    k_d = k_d_;
    k_i = k_i_;
    sum_i = 0;
    input_0 = 0;
}

void PID::update (float i_){
    input = i_;
    sum_i += i_;
    output = k_p * input + k_d * (input - input_0) + k_i * sum_i;
    input_0 = input;
}

void PID::reset_I(){
    sum_i = 0;
}


