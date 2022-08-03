#!/usr/bin/env python3
import socket

class Client():
  def __init__(self):
    self.host, self.port = '192.168.4.1', 9001
    self.test()

  def test(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((self.host, self.port))
    dat = None
    while dat is None:
      dat = s.recv(1024)
      if not dat: break
    print(dat)
    s.close()

if __name__ == '__main__':
  x = Client()
