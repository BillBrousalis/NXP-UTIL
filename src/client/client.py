#!/usr/bin/env python3
def check(func):
  def wrapper(*args, **kwargs):
    if args[0].sock is None: raise Exception(f"[-] Socket is <None>. Can't {str(func)}")
    return func(*args, **kwargs)
  return wrapper

class Client():
  def __init__(self, host: str, port: int):
    print('[*] Starting Client...')
    print(f'[*] IP: {host} | PORT: {port}')
    self.HOST, self.PORT = host, port
    self.sock = None
    self._setup()

  @property
  def sock(self):
    return self._sock

  @sock.setter
  def sock(self, s):
    self._sock = s

  def _setup(self):
    import socket
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[*] Attempting to connect to server...')
    try:
      self.sock.connect((self.HOST, self.PORT))
    except ConnectionRefusedError as e:
      self.sock = None
      print(f'[-] ConnectionRefusedError:\n{e}')
    print('[*] Connection Successfull')
  
  @check
  def close(self):
    self.sock.close()

  @check
  def readbytes(self, n: int):
    return self.sock.recv(n)

  @check
  def send(self, dat):
    if not isinstance(dat, bytes): dat = dat.encode()
    self.sock.send(dat)

  def test(self):
    self.send('Hello World')
    self.close()

if __name__ == '__main__':
  print('[ Running Client Test ]')
  c = Client('192.168.1.83', 9001)
  c.test()
elif __name__ == 'client':
  print('[+] CLIENT module added')
