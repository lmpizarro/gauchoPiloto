/*By Chris Anderson & Jordi Munoz*/
/*ArduPilot Beta 2*/
/*Feb/18/2009*/
/*Released under an Apache 2.0 open source license*/
/*Project home page is at DIYdrones.com (and ArduPilot.com)
/*We hope you improve the code and share it with us at DIY Drones!*/


#include "defs.h"

/*******************************/
//Defining waypoints variables
float wp_lat[waypoints+1];
float wp_lon[waypoints+1];
int wp_alt[waypoints+1];
unsigned char current_wp=1; //This variables stores the actual waypoint we are trying to reach.. 
unsigned char jumplock_wp=0; //When switching waypoints this lock will allow only one transition..
unsigned int wp_distance=0; //Stores the distances from the current waypoint

int  course=0; // Course over ground...
int alt=0; //Altitude, 

unsigned char wp_home_lock=0; //
int wp_bearing=0; //Stores the bearing from the current waypoint


#include "src/ACME.cpp"
#include "src/GPS_Navigation.cpp"  
#include "src/Mission_Setup.cpp"  
#include "src/PIDControl.cpp"  
#include "src/ServoControl.cpp"
#include "src/AutoPilot.cpp"
#include "src/Init.cpp"  

void setup()
{
  init_ardupilot();
  Init_servo();//Initalizing servo, see "Servo_Control" tab. 
  //Testing servos (max and mins), we are aware of the propeller and won't spin that without warning... =)
  //test_throttle();
  test_yaw();
  setup_waypoints();//See tab "Mission_Setup"
  init_startup_parameters(); //
 
}

void loop()
{
  /*************************************************************************
   * GPS function, reads and update all the GPS data... This function is located in "GPS_Navigation" tab
   *************************************************************************/
  gps_parse_nmea();

  /*************************************************************************
   *************************************************************************/
  if((gps_new_data_flag&0x01)==0x01)//Checking new GPS "GPRMC" data flag in position 
  {
    digitalWrite(13,HIGH); 
    gps_new_data_flag&=(~0x01); //Clearing new data flag... 

    yaw_control(); //This function is located in "AutoPilot" tab. 

    if(get_gps_dist(lat, lon, wp_lat[0], wp_lon[0]) > distance_limit) //If the distance from home is greater than 2000 meters
    {
      current_wp=0; //Return home... 
    } 
    /*Print values, just for debugging*/
      send_to_ground(); 
  }

  /*************************************************************************/
  /*************************************************************************/
  if((gps_new_data_flag&0x02)==0x02)///Checking new GPS "GPGGA" data flag
  {
    gps_new_data_flag&=(~0x02); //Clearing flag

    throttle_control(); //This function is located in "AutoPilot" tab. 
  }

  /*************************************************************************/
  /*This is just a prototype, ensure that the autopilot will jump ONLY ONE waypoint, checks RTL mode */
  /*************************************************************************/
  if(RTL==0)//Verify the RTl option (0=Waypoint mode, 1 = Return Home mode)
  {
    if((wp_distance<30)&&(jumplock_wp==0x00))//Checking if the waypoint distance is less than 30, and check if the lock is open
    {
      current_wp++; //Switch the waypoint
      jumplock_wp=0x01; //Lock the waypoint switcher.
      if(current_wp>waypoints)//Check if we've passed all the waypoints, if yes will return home.. 
      {
        current_wp=0; 
      }
    }

    if(digitalRead(4) == LOW) //Checks the MUX pin to see if we are in manual mode (Low = manual) 
    {
      reset_PIDs(); //Reset all the PIDs
      middle_measurement_lock=0; //status flag, to lock the starting position of the throttle
    }

  }
  else //RTL set
  {
    if(digitalRead(4) == LOW)//Checks the MUX pin to see if we are in manual mode (Low = manual)
    {
      //updates the altitude till we switch to automode, then the autopilot will try to mantain that altitude
      wp_alt[0]=alt; 
      //Reset all the PIDs
      reset_PIDs(); 
      //unlocks the starting positions of throttle and yaw. See the function in "AutoPilot" tab, inside the throttle_control() function
      middle_measurement_lock=0; 
    }
    current_wp=0; //Reseting to home waypoint, just to be sure.. 
  }

  digitalWrite(13,LOW);//Turning off the status LED
}
