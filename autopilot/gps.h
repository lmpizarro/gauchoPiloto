/*
* Copyright (C) 2015 Luis Maria Pizarro <lpizarro@cnea.gov.ar>
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

#ifndef GPS_H_
#define GPS_H_


class Gps {
    public:
        Gps();
	void cpRxBuffer (char *);
	void parse_nema_sentence ();
    private:
	uint8_t checksum();
        static const char *gp_rmc;
        static const char *gp_gga;
        static const char *c_sepr;
	float lat;
	float lon;
	float alt;
	float spe;
	float acc;
	float heada;
	char nema_sentence[LONG_BUFFER_RX_GPS];
};

const char *Gps::gp_rmc="GPRMC";
const char *Gps::gp_gga="GPGGA";
const char *Gps::c_sepr=",";

Gps::Gps(){

}

void Gps::cpRxBuffer(char *rxBuffer){
    uint8_t i = 0;	
    while (i < LONG_BUFFER_RX_GPS - 1){
	if (rxBuffer[i + 1]!='*'){    
            nema_sentence[i] = rxBuffer[i];
	} else {
	    break;
	}    
	i= i + 1;
    }	
}

void Gps::parse_nema_sentence(){
}

uint8_t Gps::checksum(){
    uint8_t i = 1;
    uint8_t checks = 0;
    while ((i < LONG_BUFFER_RX_GPS - 1)){
        if ( nema_sentence[i+1] != '*'){
            checks = checks ^ nema_sentence[i]; 
	} else {
	    break;
	}
        i++;
    }
    return checks;
}

#endif /*GPS_H_*/
