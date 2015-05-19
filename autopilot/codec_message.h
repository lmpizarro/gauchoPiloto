/*
 * * Copyright (C) 2015 Luis Maria Pizarro <lmpizarro@gmail.com>
 * *
 * * This file is part of gauchopiloto.
 * *
 * * gauchopiloto is free software; you can redistribute it and/or modify
 * * it under the terms of the GNU General Public License as published by
 * * the Free Software Foundation; either version 2, or (at your option)
 * * any later version.
 * *
 * * gauchopiloto is distributed in the hope that it will be useful,
 * * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * * GNU General Public License for more details.
 * *
 * * You should have received a copy of the GNU General Public License
 * * along with Paparazzi; see the file COPYING. If not, see
 * * <http://www.gnu.org/licenses/>.
 * */

#ifndef DECODE_MESSAGE_H_
#define DECODE_MESSAGE_H_

class decode_message {
    public:
        char mensaje [LONG_BUFFER_RX_GPS]; //= "#01040064FFFF002D0043D3!";
        uint8_t values [LONG_BUFFER_RX_GPS];
        uint16_t nums[4];
        uint8_t cks [2];
        bool error_;
        uint8_t sys_i;
        uint8_t ope_i;
        uint8_t cks_i; 
        uint8_t hex_to_int (char c);
        bool check_in_range (char c);
        void set_values ();
        bool set_nums ();
	decode_message();
    private:
};

decode_message::decode_message(){
}

uint8_t decode_message::hex_to_int (char c){
     uint8_t a = c;	
     if (c >= 48 && c <= 57) a = a - 48;
     if (c >= 65 && c <= 70) a = a - 55;

     return a;
}

bool decode_message::check_in_range (char c){
    if (c >= 48){
	if (c <= 70){
	    if (c > 57 ){
	        if (c < 65){
		    return true; 
	        }	   
	    } 
	}else{
	    return true; 
	}   
    }else{
	return true; 
    } 
    return false;
}

void decode_message::set_values (){
    for (uint8_t i = 1; i < strlen(mensaje) - 1; i++){
        values [i -1] = hex_to_int(mensaje[i]);	  
    }
    sys_i = values[0] * 16 + values [1];
    ope_i = values[2] * 16 + values [3];
    nums[0] = values[4]*4096  + values[5]*256 + values[6]*16 + values[7];
    nums[1] = values[8]*4096  + values[9]*256 + values[10]*16 + values[11];
    nums[2] = values[12]*4096  + values[13]*256 + values[14]*16 + values[15];
    nums[3] = values[16]*4096  + values[17]*256 + values[18]*16 + values[19];
    cks_i = values[20] * 16 + values [21];
}

bool decode_message::set_nums (){
    for (uint8_t i = 1; i < strlen(mensaje) - 1; i++){
        error_ = check_in_range(mensaje[i]);
	if (error_) break;
    }
    if (!error_) set_values ();
    return error_;
}


#define LEN_MENSAJE_TIPO_1  24 // 1 start, sys, ope, 4 * 4   bytes datos, cks, 1 end 
class encode_message {
    public:
        void uint8_to_2nibles (uint8_t num);
        void uint16_to_4nibles (uint16_t num);
        void set_buffer ();
	void set_sys(uint8_t);
	void set_ope(uint8_t);
        uint8_t buffer_tx [LONG_BUFFER_RX_GPS];
	static const char *hexas;
        uint8_t _4nibbles [4];
        uint8_t _2nibbles [2];

        uint16_t  num[4];
        uint8_t   sys;
        uint8_t   ope;
	uint8_t   cks;

    private:
	void set_cks();
};

const char *encode_message::hexas= "0123456789ABCDEF"; //{'0','1','2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
void encode_message::uint8_to_2nibles (uint8_t num){
   uint8_t t = num;
   _2nibbles[1] = hexas[t & 0xF];
   t = num >> 4;
   _2nibbles[0] = hexas[t & 0xF];

}

void encode_message::uint16_to_4nibles (uint16_t num){
   uint16_t t = num;
   _4nibbles[3] = hexas[t & 0xF];
   t = num >> 4;
   _4nibbles[2] = hexas[t & 0xF];
   t = num >> 8;
   _4nibbles[1] = hexas[t & 0xF];
   t = num >> 12;
   _4nibbles[0] = hexas[t & 0xF];
}

void encode_message::set_buffer (){
    uint8_t j = 0;
    buffer_tx[j] = '#'; j++;
    uint8_to_2nibles(sys);
    buffer_tx[j] = _2nibbles[0]; j++;
    buffer_tx[j] = _2nibbles[1]; j++;
    uint8_to_2nibles(ope);
    buffer_tx[j] = _2nibbles[0]; j++;
    buffer_tx[j] = _2nibbles[1]; j++;
    uint16_to_4nibles(num[0]);
    buffer_tx[j] = _4nibbles[0]; j++;
    buffer_tx[j] = _4nibbles[1]; j++;
    buffer_tx[j] = _4nibbles[2]; j++;
    buffer_tx[j] = _4nibbles[3]; j++;
    uint16_to_4nibles(num[1]);
    buffer_tx[j] = _4nibbles[0]; j++;
    buffer_tx[j] = _4nibbles[1]; j++;
    buffer_tx[j] = _4nibbles[2]; j++;
    buffer_tx[j] = _4nibbles[3]; j++;
    uint16_to_4nibles(num[2]);
    buffer_tx[j] = _4nibbles[0]; j++;
    buffer_tx[j] = _4nibbles[1]; j++;
    buffer_tx[j] = _4nibbles[2]; j++;
    buffer_tx[j] = _4nibbles[3]; j++;
    uint16_to_4nibles(num[3]);
    buffer_tx[j] = _4nibbles[0]; j++;
    buffer_tx[j] = _4nibbles[1]; j++;
    buffer_tx[j] = _4nibbles[2]; j++;
    buffer_tx[j] = _4nibbles[3]; j++;
    set_cks();
    uint8_to_2nibles(cks);
    buffer_tx[j] = _2nibbles[0]; j++;
    buffer_tx[j] = _2nibbles[1]; j++;
    buffer_tx[j] = '!';
}

void encode_message::set_sys(uint8_t sys_){sys = sys_;};
void encode_message::set_ope(uint8_t ope_){ope = ope_;};
void encode_message::set_cks(){
    	
    uint16_t  sum = num[0] + num[1] + num[2] + num[3];
    cks = (uint8_t) sum;
};

#endif /*DECODE_MESSAGE_H_*/
