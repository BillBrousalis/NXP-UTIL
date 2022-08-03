#!/usr/bin/env python3
import socket

class Server():
  MAX_DEV = 1
  def __init__(self):
    print("[*] Starting Server...")
    self.host, self.port = '', 9001
    self.sock = None
    self.clients = []
    self._setup()

  def _setup(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.sock.listen(self.MAX_DEV)
    self.accept_connections()

  def accept_connections(self):
    for i in range(self.MAX_DEV):
      conn, addr = self.sock.accept()
      self.clients.append(conn)
      print(f"[+] New Client Connected: [ {addr[0]} : {addr[1]} ]")
    print("[*] Expected number of devices have been connected")
  
  def close(self):
    if self.sock is None: raise Exception("Socket is <None>: Can't <close>")
    self.sock.close()

  def send(self, dat):
    if self.sock is None: raise Exception("Socket is <None>: Can't <send>")
    if not isinstance(dat, bytes): dat = dat.encode()
    for conn in self.clients:
      conn.send(dat)

  def test(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.host, self.port))
      s.listen(1)
      conn, addr = s.accept()
      with conn:
        print(f"Connected by {addr}")
        while 1:
          dat = conn.recv(1024)
          if not dat: break
          print(dat)

if __name__ == "__main__":
  #--testing
  s = Server()
  s.send(b'eimai o server kalispera')
  s.close()
  #s.test()
