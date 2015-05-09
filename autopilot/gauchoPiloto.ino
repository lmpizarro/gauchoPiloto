#include "pid.h"
#include "defs.h"
#include "protocol.h"
#include "time_scheduling.h"


floatToHex fToH(1.0, 2.0, 2);
floatToHex yaw(1.0, 2.0, 2);
floatToHex pitch(1.0, 2.0, 2);
floatToHex roll(1.0, 2.0, 2);
PID  c1(1,1,1);
PID  c2(1,1,1);
PID  c3(1,1,1);


unsigned long intervalSOH=1000;  // the time we need to wait
unsigned long intervalControl=100;  // the time we need to wait
Tarea SOH(intervalSOH);
Tarea Control(intervalControl);

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(HARD_BAUD_RATE);
}

uint16_t i = 0;
void loop()
{
    uint32_t intf;

// Nothing will change until millis() increments by 1000
 if (SOH.ejecutar()) {
        Serial.write("---------------------SOH");
        Serial.write('\n');
  } 

 if (Control.ejecutar()) {
        i = i + 1; 
	if (i > 100) i=0;
        intf = fToH.floatToInt(1.0 + i*0.01);
        fToH.intToHex(intf);
        intf = yaw.floatToInt(1.0 + i*0.01);
        yaw.intToHex(intf);
        intf = pitch.floatToInt(1.0 + i*0.01);
        pitch.intToHex(intf);
        intf = roll.floatToInt(1.0 + i*0.01);
        roll.intToHex(intf);

	c1.update(1);
	c2.update(1);
	c3.update(1);

	//Serial.print(1.0 + i*0.01);
	//Serial.print( "   ");
        Serial.write(fToH.hexs);
        Serial.write('\n');

	//Serial.print( "   ");
        //Serial.println(intf);
    }
}
