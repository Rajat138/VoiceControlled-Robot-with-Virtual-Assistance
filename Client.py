import socket


class Client:
    def __init__(self, ip, port):
        self.SERVER_IP = ip
        self.PORT = port
        self.socket = socket.socket()
        self.socket.connect((self.SERVER_IP, self.PORT))

    def send_msg(self, msg):
        msg = msg.encode()
        self.socket.send(msg)
