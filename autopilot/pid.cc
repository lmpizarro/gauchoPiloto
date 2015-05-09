#include "pid.h"

PID::PID (float k_p_, float k_d_, float k_i_){
    k_p = k_p_;
    k_d = k_d_;
    k_i = k_i_;
    sum_i = 0;
    input_0 = 0;
}

void PID::update (float i_){
    input = i_;
    sum_i += i_;
    output = k_p * input + k_d * (input - input_0) + k_i * sum_i;
    input_0 = input;
}

void PID::reset_I(){
    sum_i = 0;
}


