#ifndef DEFS_H_
#define DEFS_H_

//Defining ranges of the servos (and ESC), must be +-90 degrees. 
#define max16_throttle 2100 //ESC max position, given in useconds, in my ungly servos 2100 is fine, you can try 2000..
#define min16_throttle 1000 //ESC position 

#define max16_yaw 2100 //Servo max position
#define min16_yaw 1000 //Servo min position

#define reverse_yaw 1 // normal = 0 and reverse = 1

//PID max and mins
#define   heading_max 30
#define   heading_min -30

#define   altitude_max 40
#define   altitude_min -45

//Number of waypoints defined
#define   waypoints 6

#define distance_limit 4000 //The max distance allowed to travel from home.  

/*************************************************************************
 * RTL, if its set as true by the user, the autopilot will always 
 * just return to the launch lat/lon (way_lat[0], way_lon[0]) when enabled, 
 * maintaining initial altitude
 **************************************************************************/
#define RTL 1 //0 = waypoint mode, 1 = Return home mode

//PID gains
//At the begining try to use only proportional.. 
//The original configuration works fine in my simulator.. 
#define Kp_heading 10
#define Ki_heading .01
#define Kd_heading 0.001

#define Kp_altitude 4
#define Ki_altitude 0.001
#define Kd_altitude 2

#endif
