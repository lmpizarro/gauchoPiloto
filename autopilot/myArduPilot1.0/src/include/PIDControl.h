#ifndef PIDCONTROL_H_
#define PIDCONTROL_H_

/*******************************/
//PID loop variables
int heading_previous_error; 
float heading_I; //Stores the result of the integrator
int altitude_previous_error;
float altitude_I; //Stores the result of the integrator

//PID K constants, defined at the begining of the code
const float  kp[]={Kp_heading,Kp_altitude};	
const float  ki[]={Ki_heading,Ki_altitude};	 
const float  kd[]={Kd_heading,Kd_altitude};




/****************************************************************************************
 * PID= P+I+D
 ***************************************************************/
int PID_heading(int PID_error);
/* ---------------------------------------------------------------------------*/

/* ---------------------------------------------------------------------------*/


int PID_altitude(int PID_set_Point, int PID_current_Point);
/*************************************************************************
 * Reset all the PIDs
 *************************************************************************/
void reset_PIDs(void);

#endif
