#ifndef GPSNAVIGATION_H_
#define GPSNAVIGATION_H_


/*******************************/
/*GPS Pointers*/
char *token;
char *search = ",";
char *brkb, *pEnd;

//GPS obtained information
unsigned char fix_position=0;//Valid gps position
float lat=0; //Current Latitude
float lon=0; //Current Longitude
unsigned char ground_speed=0; //Ground speed? yes Ground Speed.



char buffer[90]; //Serial buffer to catch GPS data

/*************************************************************************
 * This functions parses the NMEA strings... 
 * Pretty complex but never fails and works well with all GPS modules and baud speeds.. :-) 
 * Just change the Serial.begin() value in the first tab for higher baud speeds
 *************************************************************************/

void gps_parse_nmea(void);
/*************************************************************************
 * //Function to calculate the course between two waypoints
 * //I'm using the real formulas--no lookup table fakes!
 *************************************************************************/
int get_gps_course(float flat1, float flon1, float flat2, float flon2);
/*************************************************************************
 * //Function to calculate the distance between two waypoints
 * //I'm using the real formulas
 *************************************************************************/
unsigned int get_gps_dist(float flat1, float flon1, float flat2, float flon2);

#endif
