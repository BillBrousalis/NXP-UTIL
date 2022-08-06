#!/usr/bin/env python3
import socket

class Client():
  def __init__(self, host="192.168.1.10", port=9001):
    print("[*] Starting Client...")
    self.HOST, self.PORT = host, port
    self.sock = None
    self._setup()
    self.test()

  def _setup(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.HOST, self.PORT))
    print("[*] Connection Successfull")

  def close(self):
    if self.sock is None: raise Exception("[-] Sock is None. Can't <close>")
    self.sock.close()

  def readbytes(self, n=1):
    if self.sock is None: raise Exception("[-] Sock is None. Can't <readbytes>")
    return self.sock.recv(n)

  def send(self, dat):
    if self.sock is None: raise Exception("[-] Sock is None. Can't <send>")
    if not isinstance(dat, bytes): dat = dat.encode()
    self.sock.send(dat)

  def test(self):
    self.send("Hello World")
    self.close()

if __name__ == '__main__':
  c = Client()
  c.test()
