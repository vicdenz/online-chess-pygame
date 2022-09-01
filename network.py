import socket
import const

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (socket.gethostbyname(socket.gethostname()), const.PORT)
        self.id = self.connect()
        print("[NEW CLIENT] server id:", self.id)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

n = Network()
print(n.send("hello"))
print(n.send("working"))