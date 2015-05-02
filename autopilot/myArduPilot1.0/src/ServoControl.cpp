#include "pins_arduino.h"
#include "include/ServoControl.h"

/**************************************************************
* Configuring the PWM hadware... If you want to understand this you must read the Data Sheet of atmega168..  
***************************************************************/
void Init_servo(void)//This part will configure the PWM to control the servo 100% by hardware, and not waste CPU time.. 
{   
    digitalWrite(10,LOW);//Defining servo output pins
    pinMode(10,OUTPUT);
    digitalWrite(9,LOW);
    pinMode(9,OUTPUT);
    /* Timer 1 settings for fast PWM */
    // Note: these strange strings that follow, like OCRI1A, are actually predefined Atmega168 registers. 
    // We load the registers and the chip does the rest.
    
    //Remember the registers not declared here remains zero by default... 
    TCCR1A =((1<<WGM11)|(1<<COM1B1)|(1<<COM1A1)); //Please read page 131 of DataSheet, we are changing the registers settings of WGM11,COM1B1,COM1A1 to 1 thats all... 
    TCCR1B = (1<<WGM13)|(1<<WGM12)|(1<<CS11); //Prescaler set to 8, that give us a resolution of 2us, read page 134 of data sheet
    OCR1A = 2500; //the period of servo 1, remember 2us resolution, 2500/2 = 1250us the pulse period of the servo...    
    OCR1B = 3000; //the period of servo 2, 3000/2=1500 us, more or less is the central position... 
    ICR1 = 40000; //50hz freq...Datasheet says  (system_freq/prescaler)/target frequency. So (16000000hz/8)/50hz=40000, 
                  //must be 50hz because is the servo standard (every 20 ms, and 1hz = 1sec) 1000ms/20ms=50hz, elementary school stuff... 
}

/**************************************************************
* Function to pulse the throttle servo
***************************************************************/
void pulse_servo_throttle(long angle)//Will convert the angle to the equivalent servo position... 
{
 //angle=constrain(angle,180,0);
 OCR1A=((angle*(max16_throttle-min16_throttle))/180L+min16_throttle)*2L;
}

/**************************************************************
* Function to pulse the yaw/rudder servo... 
***************************************************************/
void pulse_servo_yaw(long angle)//Will convert the angle to the equivalent servo position... 
{
 //angle=constrain(angle,180,0);
 OCR1B=((angle*(max16_yaw-min16_yaw))/180L+min16_yaw)*2L; //Scaling
}
/**************************************************************
* Function to test the servos.. 
***************************************************************/
    
    
/**************************************************************
* Improved PulseIn by Michal Bacik.. 
***************************************************************/


// Same as pulseIn, but tweaked for range 1000 - 2000 usec, and reading only HIGH phase.
// Must be compiled in .cpp file, with -Os compiler switch.
unsigned long PulseIn(uint8_t pin, unsigned long timeout){
  const uint8_t bit = digitalPinToBitMask(pin), port = digitalPinToPort(pin);
  unsigned long width = 1;
   
  unsigned long numloops = 0;
  const unsigned long maxloops = microsecondsToClockCycles(timeout) / 16;

   noInterrupts();
   //wait for the pulse to start
   while((*portInputRegister(port) & bit) != bit){
      if(++numloops == maxloops){
         interrupts();
         return 0;
      }
   }
                              //wait for the pulse to stop
   while((*portInputRegister(port) & bit) == bit)
      width++;
   interrupts();
   return clockCyclesToMicroseconds((width*0xd00L+0x800L)/256L);
}
    
    
void test_throttle(void){
 
  pulse_servo_throttle(45);
  digitalWrite(13, HIGH);
  delay(1000);
  pulse_servo_throttle(135);
  digitalWrite(13, LOW);
  delay(1000);
  digitalWrite(13, HIGH);
  pulse_servo_throttle(90);
  delay(1000);
      
}
    
void test_yaw(void)
{
  pulse_servo_yaw(90+heading_min);
  digitalWrite(13, HIGH);
  delay(1500);
  pulse_servo_yaw(90+heading_max);
  digitalWrite(13, LOW);
  delay(1500);
  digitalWrite(13, HIGH);
  pulse_servo_yaw(90);
  delay(1500);
      
}
