#!/usr/bin/env python3
def check(func):
  def wrapper(*args):
    if args[0].sock is None: raise Exception(f"[-] Socket is <None>. Can't {str(func)}")
    return func(*args)
  return wrapper

class Client():
  def __init__(self, host="192.168.1.10", port=9001):
    print("[*] Starting Client...")
    self.HOST, self.PORT = host, port
    self.sock = None
    self._setup()

  def _setup(self):
    import socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.HOST, self.PORT))
    print("[*] Connection Successfull")

  @check
  def close(self):
    self.sock.close()

  @check
  def readbytes(self, n=1):
    return self.sock.recv(n)

  @check
  def send(self, dat):
    if not isinstance(dat, bytes): dat = dat.encode()
    self.sock.send(dat)

  def test(self):
    self.send("Hello World")
    self.close()

if __name__ == '__main__':
  c = Client()
  c.test()