import socket
import struct

IP = "127.0.0.1"
PORT = 520


class Receiver:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))

    def receive(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(f" received message is : {data}")


if __name__ == "__main__":
    recv = Receiver()
    recv.receive()
