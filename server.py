import socket
from _thread import *
import uuid
import const

def threaded_client(conn, addr):
    conn.send(str.encode(str(uuid.uuid4())))

    reply = ""

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("[DISCONNECTED] from client:", addr)
                break
            else:
                print("[RECEIVED] from client:", reply)
                print("[SENDING] to client:", reply)

            conn.sendall(str.encode(reply))

        except:
            break
    
    print("[LOST CONNECTION]")
    conn.close()

def start():
    server = socket.gethostbyname(socket.gethostname())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server, const.PORT))
        s.listen(2)

        print("[STARTED] server.")
        print("[WAITING] for connection.")

        while True:
            conn, addr = s.accept()
            print("[CONNECTED] to new client:", addr)

            start_new_thread(threaded_client, (conn, addr))

if __name__ == "__main__":
    start()