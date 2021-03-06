/*
* Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
*
* This file is part of gauchopiloto.
*
* gauchopiloto is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2, or (at your option)
* any later version.
*
* gauchopiloto is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with gauchoPiloto; see the file COPYING. If not, see
* <http://www.gnu.org/licenses/>.
*/

#include "defs.h"
#include "pid.h"
#include "float_to_int.h"
#include "multiTareas.h"
#include "BufferRx.h"
#include "gps.h"
#include "navigation.h"
#include "codec_message.h"

floatToInt16 air_speed(1.0, 2.0);
floatToInt16 yaw(1.0, 2.0);
floatToInt16 pitch(1.0, 2.0);
floatToInt16 roll(1.0, 2.0);

BufferRx  b_rx(Serial); //   // 10 = 0x0A = LF

decode_message dec_mess;
encode_message enc_mess;

PID  c1(1,1,1);
PID  c2(1,1,1);
PID  c3(1,1,1);

Gps  gnav;

Nav_Point wp1(50,50,100);
Nav_Point wp2(51,51,200);
Navigation nv;


uint16_t intervalSOH=2000;  // the time we need to wait
uint16_t intervalControl=20;  // the time we need to wait
uint16_t intervalRx=50;  // the time we need to wait
Tarea SOH(intervalSOH);
Tarea Control(intervalControl);
Tarea serRx(intervalRx);
Tarea controlLento(1000);

void control_task (){
    if (Control.ejecutar()) {
    	c1.update(1);
	c2.update(1);
	c3.update(1);

    }
}

void control_lento (){
    if (controlLento.ejecutar()) {
	c3.update(1);

    }
}


uint16_t i = 0;
void soh_task(){
    if (SOH.ejecutar()) {
    i = i + 1; 
	if (i > 100) i=0;
        enc_mess.num[0] = air_speed.floatToInt(1.0 + i*0.01);
        enc_mess.num[1] = yaw.floatToInt(1.0 + i*0.01);
        enc_mess.num[2] = pitch.floatToInt(1.0 + i*0.01);
        enc_mess.num[3] = roll.floatToInt(1.0 + i*0.01);

        enc_mess.set_ope(1);
        enc_mess.set_buffer();

	Serial.write (enc_mess.buffer_tx, LEN_MENSAJE_TIPO_1);
	Serial.write ('\n');
    } 
}

void rx_task(){
    bool error;
    if (serRx.ejecutar()) {
        b_rx.recMsg ();
        if (b_rx.hasMsg()){
            strcpy (dec_mess.mensaje, b_rx.buffer_rx);
	    if (!dec_mess.set_nums()) Serial.write("#0103eeee!");
	    b_rx.reset();
	}
    }
}

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(HARD_BAUD_RATE);
    b_rx.set_limits('#', '!');
    enc_mess.set_sys(1);
}



void loop()
{

    rx_task();
    control_task();
    soh_task();
    control_lento ();
}
