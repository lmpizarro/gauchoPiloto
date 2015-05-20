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

#include "nav_point.h"
#include <math.h>

float Nav_Point::grad_to_rad ( float grad){
    return M_PI*grad/180.0;
}

Nav_Point::Nav_Point (float lat_, float lon_, float alt_){
    lat = grad_to_rad(lat_);
    lon = grad_to_rad(lon_);
    alt = grad_to_rad(lat_);
}

float Nav_Point::get_lon(){
    return lon;
}

float Nav_Point::get_lat(){
    return lat;
}



