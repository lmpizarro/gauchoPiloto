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

#include "navigation.h"
#include <math.h>

// http://embeddedgurus.com/stack-overflow/2011/02/efficient-c-tip-13-use-the-modulus-operator-with-caution/
const uint32_t Navigation::R = 6352752;
Navigation::Navigation (){
}

// distancia en metros
uint32_t Navigation::distance (Nav_Point wp2, Nav_Point wp1){
	float dLon, dLat, a, c;

	dLon = wp2.get_lon() - wp1.get_lon();
	dLat = wp2.get_lat() - wp1.get_lat();

        a = sin(dLat / 2) * sin(dLat / 2)
	        + cos(wp1.get_lat()) * cos(wp2.get_lat()) \
		        * sin(dLon / 2) * sin(dLon / 2);
        c = 2 * atan2(sqrt(a), sqrt(1 - a));

	return R*c;

}

float Navigation::bearing (Nav_Point wp2, Nav_Point wp1){
	float dLon, x, y, grad , grad1;

	dLon = wp2.get_lon() - wp1.get_lon();

	y = sin(dLon) * cos(wp2.get_lat());

	x = cos(wp1.get_lat()) * sin(wp2.get_lat())
		- sin(wp1.get_lat()) * cos(wp2.get_lat()) * cos(dLon) ;

	b_current = atan2(y,x);
	grad =  ((b_current * 180.0/M_PI) + 360);
	while (grad > 0){
	    grad1 = grad;	
            grad = grad - 360;	
	}
	return (grad1);
}

// if theta < 0 doblar a la izquierda
float Navigation::calc_turn (float b_target){
    float theta;
    float diff = b_target - b_current;
    bool neg = diff < 0;
    bool big = fabsf(diff) > M_PI;

    if (!neg && !big) theta = diff;
    if (!neg && big)  theta = -1*(2 * M_PI - diff);
    if (neg && !big)  theta =  diff;
    if (neg && big)  theta = (2 * M_PI - fabs(diff));

    return theta;
}
