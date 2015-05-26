import comm_ports
import threading
import queue_io
import redis
import time
import codec_message


class proxy_serial:
    def __init__(self, redis_server_addr, serial_port, baud_rate, start, end):
        self.redis_server_addr = redis_server_addr
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.start = start
        self.end = end

        self.redis_server = redis.Redis(self.redis_server_addr)
        self.redis_subscriber = self.redis_server.pubsub()
        self.redis_subscriber.subscribe("serial_write")

        self.ser_com = comm_ports.serial_port(self.start, self.end, self.baud_rate, self.serial_port)
        self.parser = codec_message.decode_message()

    def queue_to_ser(self):
        for m in self.redis_subscriber.listen():
            channel = m['channel']
            data =  m['data']
            if channel == "serial_write":
                self.ser_com.send_message(data)

    def ser_to_queue(self):
        while True:
            time.sleep (0.002)
            n_error = self.ser_com.receive_mesg(self.parser)
            if n_error:
                pass
                #enviar mensajes a la cola de mensajes en parser.info['mess']
                self.redis_server.publish("serial_read", self.parser.info['mess'])

    def write (self, m):
        self.redis_server.publish("serial_write", m)

    def run (self):
        tr_queue_to_ser = threading.Thread(target=self.queue_to_ser, args=())
        tr_queue_to_ser.setDaemon(True)
        tr_queue_to_ser.start()

        tr_ser_to_queue = threading.Thread(target=self.ser_to_queue, args=())
        tr_ser_to_queue.setDaemon(True)
        tr_ser_to_queue.start()
        print "proxy_serial running"

def main():
    ps = proxy_serial("127.0.0.1", "/dev/ttyACM0", 115200, '#','!')
    ps.run()

if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)

