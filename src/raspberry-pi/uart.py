#!/usr/bin/env python3
def check(func):
  def wrapper(*args, **kwargs):
    if args[0].ser is None: raise Exception(f"[-] Ser is <None>. Can't {str(func)}")
    return func(*args, **kwargs)
  return wrapper

class Uart():
  def __init__(self, uartdev: str, baud: int):
    self.ser = None
    self.DEV, self.BAUD = uartdev, baud
    self._setup()

  def _setup(self):
    import serial
    self.ser = serial.Serial(self.DEV, self.BAUD, timeout=2)
    self.ser.flush()
    print("[*] Uart Initialized")

  @check
  def close(self):
    print("[-] Closing Uart")
    self.ser.close()

  @check
  def recv(self, n: int):
    return self.ser.read(size=n)

  @check
  def send(self, dat):
    if not isinstance(dat, bytes): dat = dat.encode()
    self.ser.write(dat)

  def test(self):
    self.send("Hello World\n")
    self.close()

if __name__ == "__main__":
  print('[ Running Uart Test ]')
  u = Uart()
  u.test()
elif __name__ == 'uart':
  print('[+] UART module added')
