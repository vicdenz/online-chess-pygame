import socket
from _thread import *
import pickle
from board import Board
import const
import sys

games = []
connections = -1

def threaded_client(conn, addr, connection):
    global games, connections
    game = games[connection // 2]

    color = ""
    if game.started:
        color = game.disconnected
        game.disconnected = ""
    else:
        color = "w" if (connection % 2) == 0 else "b"
    conn.send(pickle.dumps([game, color]))

    reply = ""

    while True:
        try:
            data = conn.recv(4096)
            reply = pickle.loads(data)

            if not data:
                print("[DISCONNECTED] from client:", addr)
                break
            elif reply[0] == "select":
                game.select(reply[1])
            elif reply == "checkmate":
                checkmate = game.checkmate()
                conn.sendall(pickle.dumps(checkmate))
                continue
            elif reply == "quit":
                game.disconnected = color
                break
            conn.sendall(pickle.dumps(game))
        except:
            break
    
    print("[LOST CONNECTION]")
    if connections % 2 == 0:
        games.pop(-1)
    else:
        game.ready = False
    connections -= 1
    conn.close()

def start():
    global games, connections
    server = socket.gethostbyname(socket.gethostname())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((server, const.PORT))
        except OSError:
            print('[CONNECTION ERROR] port:'+str(const.PORT), 'already in use.')
            exit()
        s.listen(2)

        print("[STARTED] server.")
        print("[WAITING] for connection.")

        try:
            while True:
                conn, addr = s.accept()
                print("[CONNECTED] to new client:", addr)

                connections += 1

                if connections % 2 == 0:
                    games.append(Board(0, 0))
                else:
                    games[-1].ready = True

                start_new_thread(threaded_client, (conn, addr, connections))
        except KeyboardInterrupt:
            # s.shutdown(socket.SHUT_RDWR)
            s.close()
            print('[CLOSED] server closed by KeyboardInterrupt.')
            sys.exit(0)

if __name__ == "__main__":
    start()