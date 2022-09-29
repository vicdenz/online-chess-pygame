import socket
import const
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (socket.gethostbyname(socket.gethostname()), const.PORT)
        self.id = 0
        print("[NEW CLIENT] server id")

    def connect(self):
        self.client.connect(self.addr)
        response = pickle.loads(self.client.recv(4096))
        print(response)

        self.id = response[0]
        return response[1], response[2]

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            received = self.client.recv(4096)
            return pickle.loads(received)
        except socket.error as e:
            print(e)