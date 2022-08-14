#!/usr/bin/env python3
def check(func):
  def wrapper(*args, **kwargs):
    if args[0].sock is None: raise Exception(f"[-] Socket is <None>: Can't {str(func)}")
    return func(*args, **kwargs)
  return wrapper

class Server():
  def __init__(self, host: str, port: int, dev: int):
    print("[*] Starting Server...")
    self.DEV = dev
    self.HOST, self.PORT = host, port
    self.sock = None
    self.clients = []
    self._setup()

  def __str__(self):
    return ( "[DEBUG]\n"
            f"{'HOST':>15}: {self.HOST}\n"
            f"{'PORT':>15}: {self.PORT}\n"
            f"{'DEV':>15}: {self.DEV}\n"
            f"{'SOCK':>15}: {str(self.sock)}\n"
            f"{'CLIENTS':>15}: {' | '.join([str(x) for x in self.clients])}\n")

  def _setup(self):
    import socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.HOST, self.PORT))
    self.sock.listen(self.DEV)
    self.accept_connections()

  @check
  def accept_connections(self):
    for i in range(self.DEV):
      conn, addr = self.sock.accept()
      self.clients.append(conn)
      print(f"[+] New Client Connected: [ {addr[0]} : {addr[1]} ]")
    print("[*] Expected number of devices have been connected")
  
  @check
  def close(self):
    self.sock.close()

  @check
  def send(self, dat):
    if not isinstance(dat, bytes): dat = dat.encode()
    for conn in self.clients: conn.send(dat)

  def test(self):
    self.send("Hello World")
    self.close()

if __name__ == "__main__":
  #--testing
  s = Server()
  s.test()
