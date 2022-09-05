import socket
import const
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (socket.gethostbyname(socket.gethostname()), const.PORT)
        self.board, self.color = self.connect()
        print("[NEW CLIENT] server id:", self.p)

    def get_board(self):
        return self.board

    def get_color(self):
        return self.color

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(2048))

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)