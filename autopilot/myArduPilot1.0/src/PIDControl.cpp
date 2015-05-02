#include "include/PIDControl.h"


/****************************************************************************************
 * PID= P+I+D
 ***************************************************************/
int PID_heading(int PID_error)
{ 
  static unsigned int heading_PID_timer; //Timer to calculate the dt of the PID
  static float heading_D; //Stores the result of the derivator
  static int heading_output; //Stores the result of the PID loop
  float dt=(float)(millis()-heading_PID_timer)/1000;//calculating dt, you must divide it by 1000, because this system only undestands seconds.. and is normally given in millis


  //Integratior part
  heading_I+= (float)PID_error*(float)dt; //1000 microseconds / 1000 = 1 millisecond
  heading_I=constrain(heading_I,heading_min,heading_max); //Limit the PID integrator... 

  //Derivation part
  heading_D=((float)PID_error-(float)heading_previous_error)/(float)dt;

  heading_output=0;//Clearing the variable.	

  heading_output=(kp[0]*PID_error);//Proportional part, is just the KP constant * error.. and addidng to the output 
  heading_output+= (ki[0]*heading_I);//Adding integrator result...
  heading_output+= (kd[0]*heading_D);//Adding derivator result.... 

  //Adds all the PID results and limit the output... 
  heading_output = constrain(heading_output,heading_min,heading_max);//limiting the output.... 

  heading_previous_error=PID_error;//Saving the actual error to use it later (in derivating part)...

  heading_PID_timer=millis();//Saving the last execution time, important to calculate the dt...

  //Now checking if the user have selected normal or reverse mode (servo)... 
  if(reverse_yaw == 1)
  {
    return (int)(-1*heading_output); 
  }
  else
  {
    return (int)(heading_output);
  }
}
/* ---------------------------------------------------------------------------*/

/* ---------------------------------------------------------------------------*/


int PID_altitude(int PID_set_Point, int PID_current_Point)
{
  static unsigned int altitude_PID_timer;//Timer to calculate the dt of the PID
  static float altitude_D; //Stores the result of the derivator
  static int altitude_output; //Stores the result of the PID loop  

  int PID_error=0;


  float dt=(float)(millis()-altitude_PID_timer)/1000; //calculating dt, you must divide it by 1000, because this system only undestand seconds.. and is normally given in millis

  //Computes the error
  PID_error=PID_set_Point-PID_current_Point;

  //Integratior part
  altitude_I+= (float)PID_error*dt; //
  altitude_I=constrain(altitude_I,20,-20); //Limit the PID integrator... 

  //Derivation part
  altitude_D=(float)((float)PID_error-(float)altitude_previous_error)/((float)dt);

  altitude_output= (kp[1]*PID_error);//Adding proportional
  altitude_output+=(ki[1]*altitude_I);//Adding integrator result..
  altitude_output+= (kd[1]*altitude_D);//Adding Derivator result..

  //Plus all the PID results and limit the output... 
  altitude_output = constrain(altitude_output,altitude_min,altitude_max);//PID_P+PID_I+PID_D
  altitude_previous_error=PID_error;//Saving the actual error to use it later (in derivating part)...
  altitude_PID_timer=millis();//Saving the last execution time, important to calculate the dt... 
  return altitude_output; //Returns the result
}

/*************************************************************************
 * Reset all the PIDs
 *************************************************************************/
void reset_PIDs(void)
{
  heading_previous_error=0;
  heading_I=0; 

  altitude_previous_error=0;
  altitude_I=0;
}
