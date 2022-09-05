import socket
from _thread import *
import pickle
from board import Board
import const

games = []
connections = 0

def threaded_client(conn, addr, connection):
    global games, connections
    game = games[connection // 2]

    conn.send(pickle.dumps([addr, game, "w" if connection % 2 == 0 else "b"]))

    reply = ""

    while True:
        try:
            data = conn.recv(4096)
            reply = pickle.loads(data)

            if not data:
                print("[DISCONNECTED] from client:", addr)
                break
            elif reply[0] == "select":
                return conn.sendall(pickle.dumps(game.select(reply[1])))
            elif reply[0] == "checkmate":
                return conn.sendall(pickle.dumps(game.checkmate()))
        except:
            break
    
    print("[LOST CONNECTION]")
    connections -= 1
    conn.close()

def start():
    global games, connections
    server = socket.gethostbyname(socket.gethostname())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server, const.PORT))
        s.listen(2)

        print("[STARTED] server.")
        print("[WAITING] for connection.")

        while True:
            conn, addr = s.accept()
            print("[CONNECTED] to new client:", addr)

            connections += 1

            if connections % 2 == 1:
                games.append(Board(0, 0))

            start_new_thread(threaded_client, (conn, addr, connections))

if __name__ == "__main__":
    start()