#!/usr/bin/env python
import socket

HOST = "localhost"
PORT = 10000


def echo_server():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, _ = s.accept()

        while True:

            data = conn.recv(1024)
            print(data)

            if not data:
                break
            conn.sendall(data)

        conn.close()
    s.close()


if __name__ == "__main__":
    echo_server()
