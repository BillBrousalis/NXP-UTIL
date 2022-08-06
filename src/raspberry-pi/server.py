#!/usr/bin/env python3
# Simple wrapper
def check(func):
  def wrapper(*args):
    if args[0].sock is None: raise Exception(f"[-] Socket is <None>: Can't {str(func)}")
    func(*args)
  return wrapper

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
            f"{'HOST':>15}: {self.HOST}\n"
            f"{'PORT':>15}: {self.PORT}\n"
            f"{'MAX DEV':>15}: {self.MAX_DEV}\n"
            f"{'SOCK':>15}: {str(self.sock)}\n"
            f"{'CLIENTS':>15}: {' | '.join([str(x) for x in self.clients])}\n")

  def _setup(self):
    import socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.HOST, self.PORT))
    self.sock.listen(self.MAX_DEV)
    self.accept_connections()

  @check
  def accept_connections(self):
    for i in range(self.MAX_DEV):
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
