#!/usr/bin/env python3
import socket

class Client():
  def __init__(self):
    self.host, self.port = 'bill-laptop', 9001
    self.test()

  def test(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((self.host, self.port))
    s.send(b'HELLOOOOO')
    s.close()

if __name__ == '__main__':
  x = Client()
