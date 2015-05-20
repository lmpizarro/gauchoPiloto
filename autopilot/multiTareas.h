/*
* Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
*
* This file is part of gauchopiloto.
*
* gauchopilot is free software; you can redistribute it and/or modify
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

#ifndef TIME_SCHEDULING_H_
#define TIME_SCHEDULING_H_

/*
 * SEARCH: realtime arduino delay millis
 * REFS: http://nrqm.ca/mechatronics-lab-guide/lab-guide-time-triggered-scheduling/
 *       https://learn.adafruit.com/multi-tasking-the-arduino-part-1
 *       https://github.com/leomil72/swRTC
 *       http://www.leonardomiliani.com/en/2011/swrtc-un-orologio-in-tempo-reale-via-software/
 *       http://www.tigoe.com/pcomp/code/controllers/real-time-systems-and-operating-systems/
 *       http://bleaklow.com/2010/07/20/a_very_simple_arduino_task_manager.html
 * */


class Tarea {
    public:
        Tarea(uint32_t );
        bool ejecutar ();
    private:
        uint32_t interval;
	uint32_t millis_0;
};

Tarea::Tarea(uint32_t interval_){
     interval = interval_;
     millis_0 = 0;
}

bool Tarea::ejecutar (){
    if ((uint32_t)(millis() - millis_0) >= interval) {
        millis_0 = (uint32_t)millis();
        return true;
    } else {
        return false;  
    }
}



#endif /* TIME_SCHEDULING_H_*/
