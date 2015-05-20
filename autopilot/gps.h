/*
* Copyright (C) 2015 Luis Maria Pizarro <lpizarro@cnea.gov.ar>
*
* This file is part of gauchopiloto.
*
* gauchopiloto is free software; you can redistribute it and/or modify
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

#ifndef GPS_H_
#define GPS_H_
#include "defs.h"
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

class Gps {
    public:
        Gps();
	void cpRxBuffer (char *);
	void parse_nema_sentence ();
	float get_speed_ms (){return speed_knot * 0.514444;}
	float get_course (){return track;}
    private:
	char nema_sentence[LONG_BUFFER_RX_GPS];
	// Global Positioning System Fix Data 
        void parse_nema_gga();
	// Recommended Minimum sentence C
        void parse_nema_rmc();
	uint8_t checksum();
	// sentence headers
        static const char *gp_rmc;
        static const char *gp_gga;
	// token separator
        static const char *c_sepr;
        char *rest;
	char *token;

        // $GPRMC
        char status; // Status A=active or V=Void
        double lat; // 4807.038  Latitude 48 deg 07.038'
        char  ns;   // N o S
        double lon; // 01131.000  Longitude 11 deg 31.000' E
        char  ew;   // E o W
        uint32_t utc_rmc; // 123519  Fix taken at 12:35:19 UTC
        double speed_knot;  // Speed over the ground in knots  1 knot = 0.514444 m/s
        double track; // Track angle in degrees True ( Direction in degrees from north )
        // $GPGGA
	uint32_t utc_gga;
        unsigned char  qua; // Fix quality
        unsigned char  nsat;  // Number of satellites being tracked
        double hdop;  // Horizontal dilution of position
        double alt_msl;  // Altitude, Meters, above mean sea level
        double height_geoid;  // Height of geoid (mean sea level) above WGS84 ellipsoid
        // A determinar por calculo
	float acc;
};

const char *Gps::gp_rmc="$GPRMC";
const char *Gps::gp_gga="$GPGGA";
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

void Gps::parse_nema_rmc(){
        token = strtok_r(rest, c_sepr, &rest);
        utc_rmc = strtol (token, NULL, 10);
        token = strtok_r(rest, c_sepr, &rest);
        status = token[0];
        token = strtok_r(rest, c_sepr, &rest);
        lat = strtod(token, NULL);
        token = strtok_r(rest, c_sepr, &rest);
        ns = token[0];
        token = strtok_r(rest, c_sepr, &rest);
        lon = strtod (token,NULL);
        token = strtok_r(rest, c_sepr, &rest);
        ew = token[0];
        token = strtok_r(rest, c_sepr, &rest);
        speed_knot = strtod (token,NULL);
        token = strtok_r(rest, c_sepr, &rest);
        track = strtod (token,NULL);
}

void Gps::parse_nema_gga(){
        token = strtok_r(rest, c_sepr, &rest);
	utc_gga = strtol (token, NULL, 10);
        token = strtok_r(rest, c_sepr, &rest);
	//lat = strtod(token, NULL);
        token = strtok_r(rest, c_sepr, &rest);
	//ns = token[0];
        token = strtok_r(rest, c_sepr, &rest);
	//lon = strtod (token,NULL);
        token = strtok_r(rest, c_sepr, &rest);
	//ew = token[0];
        token = strtok_r(rest, c_sepr, &rest);
	qua = strtol(token, NULL, 10);
        token = strtok_r(rest, ",", &rest);
	nsat = strtol(token, NULL, 10);
        token = strtok_r(rest, c_sepr, &rest);
        if (token != NULL){
	    hdop = strtod (token,NULL);
        }
        token = strtok_r(rest, c_sepr, &rest);
        if (token != NULL){
	    alt_msl = strtod (token,NULL);
	}
        token = strtok_r(rest, c_sepr, &rest);
        if (token != NULL){
	    height_geoid = strtod (token,NULL);
	}
        token = strtok_r(rest, c_sepr, &rest);
        if (token != NULL){
	    height_geoid = strtod (token,NULL);
	}
        token = strtok_r(rest, c_sepr, &rest);
        token = strtok_r(rest, c_sepr, &rest);
}

void Gps::parse_nema_sentence(){

    char  gga [] = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47";
    char  test[] = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A";

    rest = gga;
    token = strtok_r(rest, ",", &rest);
    if (token == gp_gga){
        parse_nema_gga();
    } else {
    
        if (token == gp_rmc){
            parse_nema_rmc();   
	}
    } 
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
