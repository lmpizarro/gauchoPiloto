#include "include/AutoPilot.h"
#include "include/test.h"

/*************************************************************************
 * Throttle Control, reads gps info, executes PID and pulses the motor controller..
 *************************************************************************/
void throttle_control(void)
{

  if((middle_measurement_lock==0)&&(digitalRead(4)==HIGH))//Verify if the lock is open (equal to zero) and if we are in automode.. 
  {
    int read_servo=0; //Declaring a temporary variable
    middle_measurement_lock=1; //Locking this part of the code


    //Now reading the yaw initial position
    while(digitalRead(2) == HIGH){} //Waits until the input pin goes low.
      read_servo = pulseIn(2, HIGH); //Read the pulse length of the receiver
    middle_thr = ((read_servo-min16_throttle)*180L)/(max16_throttle-min16_throttle); //Converting the pulse to degrees... 
    //Serial.println(read_servo); //Just print values
    //Serial.println(middle_thr);

    //Now reading the yaw initial position
    while(digitalRead(3) == HIGH){} //Waits until the input pin goes low.
    read_servo=pulseIn(3, HIGH); //Reads the pulse length of signal from receiver
    middle_yaw=((read_servo-min16_yaw)*180L)/(max16_yaw-min16_yaw); //Converting the pulse to degrees... 
    //Serial.println(read_servo); //Just print values
    //Serial.println(middle_yaw);
  }

  // Central Position + PID(current altitude, desired altitude - launch altitude).  
  // The result will be the motor speed value.. 
  // I subtract the current altitude (alt) from the "launch_altitude" in order to make it realtive to the start point,
  // Example: If you launch you airp. at 300 meters above sea level, and you want to maintain 50 meters above your head, 
  // the airp. will fly at 350 meters above sea level. 
  test3 = middle_thr + PID_altitude(wp_alt[current_wp], (alt - launch_altitude));



  if ( test3 < 45 ){ //Just to limit the result
      test3=45;
  }


  pulse_servo_throttle(test3); //sending position to the motor controller... 
  //the values are given in degrees, where 45 degrees is motor off, 
  //90 degrees is middle thrust, and 135 degrees is full thrust.


}

/*************************************************************************
 * Yaw Control, reads gps info, calculates navigation, executes PID and sends values to the servo.. 
 *************************************************************************/
void yaw_control(void)
{

  //Calculating Bearing, this function is located in the GPS_Navigation tab.. 
  wp_bearing=get_gps_course(lat, lon, wp_lat[current_wp], wp_lon[current_wp]);

  //Calculating Distance, this function is located in the GPS_Navigation tab.. 
  wp_distance=get_gps_dist(lat, lon, wp_lat[current_wp], wp_lon[current_wp]); 

  test = middle_yaw + PID_heading(compass_error(wp_bearing, course)); 
  
  // Central Position + PID(compass_error(desired course, current course)). 
  // test=middle_yaw+PID_heading(compass_error(45, course));  
  // Special mode to just fly NE. Comment out line above and use this one to test autopilot 
  
  //The compass error function is located in "ACME" tab.
  pulse_servo_yaw(test);//Sending values to servo, 90 degrees is central position. 

}
