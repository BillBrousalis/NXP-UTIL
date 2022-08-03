#!/usr/bin/env python3
import socket

class Client():
    def __init__(self):
        self.test()

    def test(self):
        HOST = "localhost"  # The server's hostname or IP address
        PORT = 9001  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

            print(f"Received {data!r}")

if __name__ == "__main__":
    x = Client()

