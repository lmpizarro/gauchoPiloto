#include "include/ACME.h"
#include "include/test.h"

void send_to_ground(void)
{
    //Warning if you are using a baud rate of 4800 this will super slow down the system.. 
    /*
    Serial.print("Mot: ");
    Serial.print(test3);
    Serial.print(" Yaw: ");
    Serial.print((int)test);
    */

    /*
    Serial.print(" crs: ");   
    Serial.print(course);
    Serial.print(" WP Dir: ");
    Serial.print((int)wp_bearing);
    Serial.print(" DAlt: "); 
    Serial.print(wp_alt[current_wp]); 
    
    Serial.print(" Dst: ");
    Serial.print(wp_distance);
    Serial.print(" WP: ");
    Serial.println((int)current_wp);
    */

    /*
    Serial.print(" Alt: ");  
    Serial.print((int)alt-launch_altitude);
    Serial.print(" Crs: ");   
    Serial.print(course);
    Serial.print(" Dis: "); 
    Serial.print(wp_distance);
    Serial.print(" Des: ");
    Serial.println((int)wp_bearing);
    */
}

/**************************************************************
 * Special module to limit float values, which is like constrain() but for variables IEEE 754 (Don't worry about it, it's just a floating point variables). =)  
 * It's called "ACME" because that's the generic name for everything in the Road Runner cartoons ;-)
 ***************************************************************/

float constrain_float(float value, float max, float min)
{
  if (value > max)
  {
    value=max;
  }
  if (value < min)
  {
    value=min;
  }
  return value;
}

/***************************************************************************/
//Computes heading the error, and choose the shortest way to reach the desired heading
/***************************************************************************/
int compass_error(int PID_set_Point, int PID_current_Point)
{
   float PID_error=0;//Temporary variable
   
    if(fabs(PID_set_Point-PID_current_Point) > 180) 
	{
		if(PID_set_Point-PID_current_Point < -180)
		{
		  PID_error=(PID_set_Point+360)-PID_current_Point;
		}
		else
		{
		  PID_error=(PID_set_Point-360)-PID_current_Point;
		}
	}
	else
	{
          PID_error=PID_set_Point-PID_current_Point;
        }

	return PID_error;
}




//This function is no used.. 
int altitude_error(int PID_set_Point, int PID_current_Point)
{
  int PID_error=PID_set_Point-PID_current_Point;  
  
  return PID_error;
}


