#include <iostream>          // For cout and cerr
#include <string.h>
#include <stdint.h>

#include "defs.h"
#include "process_message.h"

bool Process_Message::process(){
    strcpy (dec_mess.mensaje, r_buffer);

    if (dec_mess.set_nums() == 0){
	if (dec_mess.ope_i == MESSAGE_SOH){
            soh_a();		
	} else if (dec_mess.ope_i == MESSAGE_REFS) {
            refs_a();		
	} else if (dec_mess.ope_i == MESSAGE_MEAS){
            meas_a();
        }
        return 0;
    } else {
        return 1;
    }
}

void Process_Message::soh_a (){
    strcpy (r_buffer, "#0101000011112222333343!");
}

void Process_Message::refs_a (){
    strcpy (r_buffer, "#0102444433332222111145!");
}

void Process_Message::meas_a (){
    strcpy (r_buffer, "#0103FFFFEEEEDDDDCCCC44!");
}
