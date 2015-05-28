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

#ifndef PROCESS_MESSAGE_H_
#define PROCESS_MESSAGE_H_

#include "codec_message.h"

/*
 * Process Message
 * */
class Process_Message{
    public:
        void soh_a ();
        void refs_a ();
        void meas_a ();
        bool process ();
        decode_message dec_mess;
	char * r_buffer;
    private:	    
};

#endif /*PROCESS_MESSAGE_H_*/
