#
#   A wrapper for C++ sockets on Unix and Windows
#   Copyright (C) 2002
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

CXX = g++
#CXXFLAGS = -Wall -ansi -pedantic -g
#CXXFLAGS=-pedantic -O3 -Wall -Wextra -Werror -I ../autopilot
CXXFLAGS=-pedantic -O3 -Wall -Wextra 
LIBS = -lpthread

ifeq ($(shell uname),SunOS)
  LIBS = -lsocket -lnsl
endif

all:  UDPServer utils.o

UDPServer: UDPServer.o PracticalSocket.o process_message.o filters.o codec_message.o
#	$(CXX) -o UDPServer  UDPServer.o PracticalSocket.o  filters.o  codec_message.o process_message.o $(LIBS)
	$(CXX) -o UDPServer UDPServer.o PracticalSocket.o codec_message.o process_message.o filters.o $(LIBS)

UDPServer.o: UDPServer.cpp PracticalSocket.cpp PracticalSocket.h filters.h process_message.h
	$(CXX) $(CXXFLAGS) -c  UDPServer.cpp

PracticalSocket.o: PracticalSocket.cpp PracticalSocket.h
	$(CXX) $(CXXFLAGS) -c  PracticalSocket.cpp

utils.o: utils.cpp utils.h
	$(CXX) $(CXXFLAGS) -c utils.cpp

process_message.o: process_message.cpp process_message.h
	$(CXX) $(CXXFLAGS) -c process_message.cpp

filters.o: filters.cpp filters.h
	$(CXX) $(CXXFLAGS) -c filters.cpp

codec_message.o: codec_message.cpp codec_message.h
	$(CXX) $(CXXFLAGS) -c codec_message.cpp



clean:
	$(RM) UDPServer *.o
