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

// REFS: http://tom.pycke.be/mav/101/circle-navigation
// http://www.deanandara.com/Argonaut/Sensors/Gps/GettingData.html

#ifndef NAVIGATION_H_
#define NAVIGATION_H_

#include "nav_point.h"
#include <stdint.h>

class Navigation{
    public:
        Navigation ();
	uint32_t distance (Nav_Point ,Nav_Point);    
	float bearing (Nav_Point ,Nav_Point);    
	float calc_turn (float);
	float b_current;
    private:
        static const uint32_t R;
};

#endif /* NAVIGATION_H_*/
