#ifndef PROTOCOL_H_
#define PROTOCOL_H_

#include "defs.h"
#include <stdint.h>

class floatToHex
{
    private:
        float minF;
        float maxF;
        uint32_t max_int;
        float p;
        float b;
        uint32_t n_byteI;
	char hexDigits [16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
    public:
	char hexs[MAX_BYTES * 2 + 1];
        floatToHex (float, float, uint32_t);
        uint32_t floatToInt (float f);
        void intToHex (uint32_t);
};




#endif /*PROTOCOL_H_*/
