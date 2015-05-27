#include <iostream>
#include <cstdlib>           // For atoi()
#include <ctime>
#include <unistd.h>
#include <sys/time.h>
#include "utils.h" 

using namespace std;

struct timeval start;

void init_millis (){
    gettimeofday(&start, NULL);
}

unsigned long millis (){

    unsigned long seconds, millis, micros;    
    struct timeval now;

    gettimeofday(&now, NULL);
    seconds  = now.tv_sec  - start.tv_sec;
    micros = now.tv_usec - start.tv_usec;
    millis = ((seconds) * 1000 + micros/1000.0) + 0.5;
    return  millis;
}

int test() {
    init_millis ();
    sleep(5); // sleep 5s

    //cout << "difference: " << millis () << endl;
    return 0;
}
