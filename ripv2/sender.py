import socket

IP = "127.0.0.1"
PORT = 520
MESSAGE = b"test message"


class Sender():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self):
        self.sock.sendto(MESSAGE, (IP, PORT))


if __name__ == "__main__":
    s = Sender()
    s.send()
