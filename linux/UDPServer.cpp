/*
 *   C++ sockets on Unix and Windows
 *   Copyright (C) 2002
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
#include <iostream>          // For cout and cerr
#include <cstdlib>           // For atoi()
#include <stdint.h>
#include <pthread.h>          // For POSIX threads 
#include <unistd.h>
#include "PracticalSocket.h" // For UDPSocket and SocketException
#include "defs.h"
#include "codec_message.h" // For UDPSocket and SocketException

#define MESSAGE_SOH   1
#define MESSAGE_REFS  2 

void *udp_server (void *);
void process_messg ();
void soh_a ();
void refs_a ();
void *filter_50(void * t);
void *filter_01(void * t);

const int ECHOMAX = 255;     // Longest string to echo
char rx_Buffer[ECHOMAX];         // Buffer for echo string
int recvMsgSize;                  // Size of received message
string sourceAddress;             // Address of datagram source
unsigned short sourcePort;        // Port of datagram source

decode_message dec_mess;

void process_messg(){
    strcpy (dec_mess.mensaje, rx_Buffer);
    uint8_t addr;
    uint8_t mess_def;

    if (dec_mess.set_nums() == 0){
        //cout << " decoded buffer "<< rx_Buffer <<endl;

	addr = dec_mess.sys_i;
        mess_def = dec_mess.ope_i;
        //cout << " addr "<< " mess_d  "<< " 0 " << " 1 " << " 2 " << " 3 " <<endl;
        cout << addr + 0 << " " << mess_def+ 0  << " " << dec_mess.nums[0] <<  " " <<  
		dec_mess.nums[1] <<  " " << dec_mess.nums[2] <<  " " << dec_mess.nums[3] << endl;
	if (mess_def == MESSAGE_SOH){
            soh_a();		
	} else if (mess_def == MESSAGE_REFS) {
            refs_a();		
	}   
        recvMsgSize = strlen(rx_Buffer);		

    }
}

void *filter_50(void * t){
    for (;;) {  // Run forever
        usleep(20000);
        //cout << " filter 50 " << endl;
    }
}

void *filter_01(void * t){
    for (;;) {  // Run forever
        usleep(1000000);
        //cout << " filter 01 " << endl;
    }
}

void soh_a (){
    strcpy (rx_Buffer, "#010100!");
}

void refs_a (){
    strcpy (rx_Buffer, "#010200!");
}

void *udp_server (void * servPort) {

     long echoServPort =  (long) servPort;

    try {
         UDPSocket sock(echoServPort);                
  
         for (;;) {  // Run forever
      //      Block until receive message from a client
           recvMsgSize = sock.recvFrom(rx_Buffer, ECHOMAX, sourceAddress, 
                                      sourcePort);
  
           //cout << "Received packet from " << sourceAddress << ":" << sourcePort << endl;
           //cout << " size " << recvMsgSize << endl;
           rx_Buffer [recvMsgSize] = '\0';
           //cout << " received buffer "<< rx_Buffer << " dec mess" << dec_mess.mensaje <<endl;

           process_messg();

           sock.sendTo(rx_Buffer, recvMsgSize, sourceAddress, sourcePort);
         }
    } catch (SocketException &e) {
         cerr << e.what() << endl;
         exit(1);
    }
    // NOT REACHED
}

int main(int argc, char *argv[]) {
    // Create client thread  
    pthread_t threadID;              // Thread ID from pthread_create()  
    pthread_attr_t attr;
    long echoServPort;
    void *status;
    int rc = 0;

    if (argc != 2) {                  // Test for correct number of parameters
        cerr << "Usage: " << argv[0] << " <Server Port>" << endl;
        exit(1);
    }

    echoServPort = atoi(argv[1]);     // First arg:  local port

    // Initialize and set thread joinable
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    // Crea el thread del servidor, recibe datos y responde al cliente
    if (pthread_create(&threadID, NULL, udp_server, (void *)echoServPort) != 0) {
            cerr << "Unable to create server thread" << endl;
            exit(1);
    }

    // Crea tl thread de un filtro que ejecuta 50 veces por segundo
    if (pthread_create(&threadID, NULL, filter_50, NULL) != 0) {
            cerr << "Unable to create filter_50 thread" << endl;
            exit(1);
    }

    // Crea tl thread de un filtro que ejecuta 50 veces por segundo
    if (pthread_create(&threadID, NULL, filter_01, NULL) != 0) {
            cerr << "Unable to create filter_01 thread" << endl;
            exit(1);
    }

    // free attribute and wait for the other threads
    pthread_attr_destroy(&attr);
    //rc = pthread_join(threadID, &status);
    if (rc){
        cout << "Error:unable to join," << rc << endl;
        exit(-1);
    }

    useconds_t usec = 1000000;

    cout << "Threads initiated" << endl;
    //server (echoServPort);

    while (1){
        usleep(10 * usec);
    }
    return 0;
}

