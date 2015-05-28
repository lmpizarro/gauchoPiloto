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
* * along with gauchoPiloto; see the file COPYING. If not, see
* * <http://www.gnu.org/licenses/>.
*/

#ifndef UDPServer_H_
#define UDPServer_H_

#include <string>          
#include "defs.h"
#include "codec_message.h" 

void *udp_server (void *);

extern const int ECHOMAX = 255;     // Longest string to echo
extern char rx_Buffer[ECHOMAX];         // Buffer for echo string
extern int recvMsgSize;                  // Size of received message
extern std::string sourceAddress;             // Address of datagram source
extern unsigned short sourcePort;        // Port of datagram source


decode_message dec_mess;

#endif /*UDPServer_H_*/
