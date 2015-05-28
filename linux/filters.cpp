#include <unistd.h>
#include "filters.h"


void *filter_50(void * t){
    int t_ = (int)t;
    t_++;
    for (;;) {  // Run forever
        usleep(20000);
        //cout << " filter 50 " << endl;
    }
}

void *filter_01(void * t){
    int t_ = (int) t;	
    t_++;
    for (;;) {  // Run forever
        usleep(1000000);
        //cout << " filter 01 " << endl;
    }
}


