#!/usr/bin/env python3
import socket

class Server():
  def __init__(self, host='', port=9001, max_dev=1):
    print("[*] Starting Server...")
    self.MAX_DEV = max_dev
    self.HOST, self.PORT = host, port
    self.sock = None
    self.clients = []
    self._setup()

  def __str__(self):
    return ( "[DEBUG]\n"
            f"HOST: {self.HOST:>10}\n"
            f"PORT: {self.PORT:>10}\n"
            f"MAX DEV: {self.MAX_DEV:>10}\n"
            f"SOCK: {self.sock:>10}\n"
            f"CLIENTS: {self.clients:>10}\n")

  def _setup(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.HOST, self.PORT))
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
    for conn in self.clients: conn.send(dat)

  def test(self):
    self.send("Hello World")
    self.close()

if __name__ == "__main__":
  #--testing
  s = Server()
  print(s)
  #s.test()
