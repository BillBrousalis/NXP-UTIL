#!/usr/bin/env python3
import socket

class Server():
  def __init__(self):
    self.host, self.port = 'fe80::106f:c39e:a20e:5e8c%4', 9001
    print(self.host, self.port)
    self.test() 

  def test(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.host, self.port))
      s.listen(1)
      conn, addr = s.accept()
      with conn:
        print(f"Connected by {addr}")
        while True:
          data = conn.recv(1024)
          if not data:
            break
          conn.sendall(data)

if __name__ == "__main__":
  #--testing
  s = Server()
