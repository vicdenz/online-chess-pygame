import socket
from _thread import *
import pickle
from board import Board
import const
import sys

#{board: {'w': conn, 'b': conn}, ...}
games = {}
connections = -1

def threaded_client(game, color, addr):
    global games, connections
    conn = games[game][color]

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
                return_code = game.select(reply[1])

                if return_code == 2:
                    other_color = const.invert_color(color)
                    print('[SEND DATA] to other client:', other_color)
                    games[game][other_color].sendall(pickle.dumps("ready"))
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
        games.pop(game)
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
                    games[Board(0, 0)] = {'w': None, 'b': None}
                    current_game = list(games.keys())[-1]
                else:
                    current_game = list(games.keys())[-1]
                    current_game.ready = True
                    games[current_game]['w'].sendall(pickle.dumps("start"))

                color = ""
                if current_game.started:
                    color = current_game.disconnected
                    current_game.disconnected = ""
                else:
                    color = "w" if (connections % 2) == 0 else "b"

                games[current_game][color] = conn

                start_new_thread(threaded_client, (current_game, color, addr))
        except KeyboardInterrupt:
            # s.shutdown(socket.SHUT_RDWR)
            s.close()
            print('[CLOSED] server closed by KeyboardInterrupt.')
            sys.exit(0)

if __name__ == "__main__":
    start()