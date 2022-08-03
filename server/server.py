#!/usr/bin/env python3
import socket

class Server():
  def __init__(self):
    self.host, self.port = '', 9001
    print(self.host, self.port)
    self.test() 

  def test(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.host, self.port))
      s.listen(1)
      conn, addr = s.accept()
      with conn:
        print(f"Connected by {addr}")
        while 1:
          dat = conn.recv(1024)
          if not dat:
            break
          print(dat)

if __name__ == "__main__":
  #--testing
  s = Server()
