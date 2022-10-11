import socket
import const
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (socket.gethostbyname(socket.gethostname()), const.PORT)
        print("[NEW CLIENT] server id:")

    def connect(self):
        self.client.connect(self.addr)
        response = pickle.loads(self.client.recv(4096))

        return response

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            received = self.client.recv(4096)
            return pickle.loads(received)
        except socket.error as e:
            print(e)