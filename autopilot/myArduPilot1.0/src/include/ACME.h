#ifndef ACME_H_
#define ACME_H_

//ACME variables
unsigned char gps_new_data_flag=0; // A simple flag to know when we've got new gps data.
unsigned int launch_altitude =0; //launch altitude, altitude in waypoints is relative to starting altitude.
int middle_thr=90; //The central position
int middle_yaw=90; //The cnetral position of yaw
unsigned char middle_measurement_lock=0; //Another lock to void resetting the middle measurement.. 
/*******************************/



void send_to_ground(void);
/**************************************************************
 * Special module to limit float values, which is like constrain() but for variables IEEE 754 (Don't worry about it, it's just a floating point variables). =)  
 * It's called "ACME" because that's the generic name for everything in the Road Runner cartoons ;-)
 ***************************************************************/

float constrain_float(float value, float max, float min);
/***************************************************************************/
//Computes heading the error, and choose the shortest way to reach the desired heading
/***************************************************************************/
int compass_error(int PID_set_Point, int PID_current_Point);



//This function is no used.. 
int altitude_error(int PID_set_Point, int PID_current_Point);

#endif /*ACME_H_*/
