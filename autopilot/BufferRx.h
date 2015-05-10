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

class BufferRx {
    private:
        char buffer_rx [LONG_BUFFER_RX];
        uint8_t flag_init;
        uint8_t flag_end;
        uint8_t pointer;
    public:
        BufferRx();
        void recMsg ();
        uint8_t hasMsg();
        void reset();
};

void BufferRx::reset(){
     pointer = 0;
     flag_end = 0;
     flag_init = 0;
}

uint8_t BufferRx::hasMsg(){
    return flag_init * flag_end;
}

BufferRx::BufferRx(){
    flag_init = 0;
    pointer = 0;
    flag_end = 0;
}

void BufferRx::recMsg ()
{
    uint16_t charAvail;
    char incomingChar;

    charAvail = Serial.available();

    while(charAvail>0){

            incomingChar = Serial.read();


            if (incomingChar == '#' && !flag_init && !pointer){
	        //pointer = 0;
                buffer_rx[pointer] = incomingChar;
		flag_init = 1;
	        pointer = pointer + 1;
            } else {
                if (incomingChar == '!' && flag_init && !flag_end && pointer){
                    buffer_rx[pointer] = incomingChar;
                    flag_end = 1;
	            pointer = pointer + 1;
                    buffer_rx[pointer] = '\0';
		} else  {
		    if (flag_init && !flag_end && (pointer < LONG_BUFFER_RX - 2 )){
                        buffer_rx[pointer] = incomingChar;
	                pointer = pointer + 1;
		    } else {
		        if (pointer > (LONG_BUFFER_RX - 1)) reset();
		    }
		}
	    }
            charAvail --;
    }
}


