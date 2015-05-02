#ifndef SERVOCONTROL_H_
#define SERVOCONTROL_H_



/**************************************************************
* Configuring the PWM hadware... If you want to understand this you must read the Data Sheet of atmega168..  
***************************************************************/
void Init_servo(void);//This part will configure the PWM to control the servo 100% by hardware, and not waste CPU time.. 
/**************************************************************
* Function to pulse the throttle servo
***************************************************************/
void pulse_servo_throttle(long angle);//Will convert the angle to the equivalent servo position... 
/**************************************************************
* Function to pulse the yaw/rudder servo... 
***************************************************************/
void pulse_servo_yaw(long angle);//Will convert the angle to the equivalent servo position... 
/**************************************************************
* Function to test the servos.. 
***************************************************************/
    
void test_yaw(void);
    
void test_throttle(void);
/**************************************************************
* Improved PulseIn by Michal Bacik.. 
***************************************************************/
#include "pins_arduino.h"
// Same as pulseIn, but tweaked for range 1000 - 2000 usec, and reading only HIGH phase.
// Must be compiled in .cpp file, with -Os compiler switch.
unsigned long PulseIn(uint8_t pin, unsigned long timeout);

#endif  
