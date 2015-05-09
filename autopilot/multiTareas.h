#ifndef TIME_SCHEDULING_H_
#define TIME_SCHEDULING_H_

/*
 * SEARCH: realtime arduino delay millis
 * REFS: http://nrqm.ca/mechatronics-lab-guide/lab-guide-time-triggered-scheduling/
 *       https://learn.adafruit.com/multi-tasking-the-arduino-part-1
 *       https://github.com/leomil72/swRTC
 *       http://www.leonardomiliani.com/en/2011/swrtc-un-orologio-in-tempo-reale-via-software/
 *       http://www.tigoe.com/pcomp/code/controllers/real-time-systems-and-operating-systems/
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
        millis_0 = (uint32_t) millis();
        return true;
    } else {
        return false;  
    }
}



#endif /* TIME_SCHEDULING_H_*/
