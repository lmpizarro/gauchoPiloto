/*
* Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
*
* This file is part of paparazzi.
*
* paparazzi is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2, or (at your option)
* any later version.
*
* paparazzi is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Paparazzi; see the file COPYING. If not, see
* <http://www.gnu.org/licenses/>.
*/


#include "defs.h"
#include "pid.h"
#include "protocol.h"
#include "multiTareas.h"
#include "BufferRx.h"
#include "gps.h"

floatToHex fToH(1.0, 2.0, 2);
floatToHex yaw(1.0, 2.0, 2);
floatToHex pitch(1.0, 2.0, 2);
floatToHex roll(1.0, 2.0, 2);
PID  c1(1,1,1);
PID  c2(1,1,1);
PID  c3(1,1,1);
BufferRx  b_rx('#', '!');   // 10 = 0x0A = LF
Gps  gnav;

unsigned long intervalSOH=1000;  // the time we need to wait
unsigned long intervalControl=100;  // the time we need to wait
unsigned long intervalRx=5;  // the time we need to wait
Tarea SOH(intervalSOH);
Tarea Control(intervalControl);
Tarea serRx (intervalRx);

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(HARD_BAUD_RATE);
}


uint16_t i = 0;
void control_task (){

    uint32_t intf;
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

void soh_task(){
    if (SOH.ejecutar()) {
        Serial.write("---------------------SOH");
        Serial.write('\n');
    } 
}

void loop()
{


    if (serRx.ejecutar()) {
        b_rx.recMsg ();
        if (b_rx.hasMsg()){
	    b_rx.reset();
            Serial.write("Hay dato");
            Serial.write('\n');
	}
    }

    control_task();
    soh_task();
}
