#ifndef AUTOPILOT_H_
#define AUTOPILOT_H_


/*************************************************************************
 * Throttle Control, reads gps info, executes PID and pulses the motor controller..
 *************************************************************************/
void throttle_control(void);
/*************************************************************************
 * Yaw Control, reads gps info, calculates navigation, executes PID and sends values to the servo.. 
 *************************************************************************/
void yaw_control(void);

#endif /*AUTOPILOT_H*/
