import os
import socket
from threading import Thread

class Proxy(Thread):
    """ used to proxy single udp connection """
    BUFFER_SIZE = 4096 

    def __init__(self, listening_address, forward_address):
        print(" Server started on", listening_address)
        Thread.__init__(self)
        self.bind = listening_address
        self.target = forward_address

    def run(self):
        # Listen for incoming connections
        target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        target.connect(self.target)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(self.bind)
        except socket.error as err:
            print(f"Couldn't bind server on {self.bind}")
            raise SystemExit
        while True:
            datagram = s.recv(self.BUFFER_SIZE)
            if not datagram:
                break
            length = len(datagram)
            sent = target.send(datagram)
            if length != sent:
                print(f'Cannot send to {self.target}, {length} != {sent}')
        s.close()


if __name__ == "__main__":
    LISTEN = ("0.0.0.0", 8008)
    
    # Use environment variable for target address
    target_env = os.getenv("TARGET_SERVER", "localhost:5084")
    target_host, target_port = target_env.split(":")
    TARGET = (target_host, int(target_port))

    while True:
        proxy = Proxy(LISTEN, TARGET)
        proxy.start()
        proxy.join()
        print(" [restarting] ")
