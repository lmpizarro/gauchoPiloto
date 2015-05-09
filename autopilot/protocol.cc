#include "protocol.h"
#include <stdint.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))


floatToHex::floatToHex (float min_, float max_, uint32_t n_byteI_ ){
    minF = min_;
    maxF = max_;
    n_byteI = n_byteI_;
    uint32_t a = 1; 
    max_int = (a << (n_byteI * 8)) -1;
    p = (float) max_int /(maxF - minF);
    b = - minF * p;

}

uint32_t floatToHex::floatToInt (float f){
  return MAX(0, MIN(f*p + b, max_int));
}

//
// Convierte un int a 4 char ascii 0 a F
//
void floatToHex::intToHex (uint32_t temp)
{
    uint32_t i;
    for (i=0; i < n_byteI * 2; i++){
        hexs[n_byteI * 2 - 1 - i] = hexDigits[temp & 0x000F];
        temp = temp >> 4;
    }
    hexs[i] = '\0';

}


