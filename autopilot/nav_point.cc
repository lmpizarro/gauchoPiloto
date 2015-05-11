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



