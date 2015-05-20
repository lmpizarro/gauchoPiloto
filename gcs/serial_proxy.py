import serial
import threading
import time
from sets import Set

hexaChars = Set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
'C', 'D', 'E', 'F', '#', '!'])

string = "45sd#fede1234ffeeaabb887767!fg"

start_ = "#"
end_  = "!"
i = 0
error = 0
mensaje = ""
flag_start = 0
flag_end = 0

serial_comm = None

MENSAJE_TIPO_1 = 1 # 4 enteros de 2 bytes
LEN_MENSAJE_TIPO_1 = 22 # 4 enteros de 2 bytes
MENSAJE_TIPO_2 = 2 # 4 enteros de 2 bytes
LEN_MENSAJE_TIPO_2 = 22 # 4 enteros de 2 bytes
MENSAJE_TIPO_3 = 3 # 4 enteros de 2 bytes
LEN_MENSAJE_TIPO_3 = 8 # 4 enteros de 2 bytes

def message_is_hexa(message):
    condition = True
    for e in message:
        condition = condition and (e in hexaChars)
    return condition    

def _4hexa_to_byte (s):
    return int(s[3],16) + 16 * int(s[2],16) + 16 * 16 * int(s[1],16) + 16*16*16 * int(s[0],16)

def _2hexa_to_byte (s):
    return int(s[1],16) + 16 * int(s[0],16)

def parse_message (message):
    mensaje = message.upper()
    len_mensaje = len(mensaje)
    if (message_is_hexa (mensaje) and len_mensaje >= 4):
        sys = mensaje[0:2]
        ope = mensaje[2:4]
        error = 0
    else:
        error = 1
    if error == 0:
        sys_i = _2hexa_to_byte(sys)
        ope_i = _2hexa_to_byte(ope)
        if ope_i == MENSAJE_TIPO_1:
            if len_mensaje == LEN_MENSAJE_TIPO_1:
                print "mensaje tipo 1 ", mensaje
                pass
        elif ope_i == MENSAJE_TIPO_2:        
            if len_mensaje == LEN_MENSAJE_TIPO_2:
                print "mensaje tipo 2 ", mensaje
                pass
        elif ope_i == MENSAJE_TIPO_3:        
            if len_mensaje == LEN_MENSAJE_TIPO_3:
                print "mensaje tipo 3 ", mensaje
                pass

def receive_mesg ():
    mensaje = ""
    while True:
        while serial_comm.inWaiting() > 0:
            c = serial_comm.read(1)
            if c == start_:
                flag_start = 1
                mensaje = ""
            elif c != end_ and flag_start == 1:
                mensaje +=c
            elif c == end_ and flag_start == 1:
                parse_message (mensaje)
                mensaje = ""


class _4ints_to_mensaje:
    def __init__(self, sys_, ope_):
        self.sys = sys_
        self.ope = ope_
        pass

    def mensaje (self, num):
        self.num = num 
        mensaje = "#" + hex(self.sys)[2:].zfill(2) + hex(self.ope)[2:].zfill(2)
        sum_num = 0
        for n in self.num:
            sum_num += n
            mensaje += hex(n)[2:].zfill(4)
        hex_sum_num = hex(sum_num)
        len_hex_sum_num = len (hex_sum_num)
        cks = hex_sum_num[len_hex_sum_num - 2:]
        mensaje = mensaje + cks + '!'
        return mensaje.upper()


if __name__ == "__main__":
    serial_comm = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        timeout=None,
        )
    
    tr = threading.Thread(target=receive_mesg)
    tr.setDaemon(True)
    tr.start()

    while True:
        time.sleep (1)
        serial_comm.write ("#0101FFFF1FFF0FFF10FFFC!")
    
    m4 = _4ints_to_mensaje(1, 4)

    num = [100, 65535, 45, 67]
    print (m4.mensaje(num))

