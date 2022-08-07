#!/usr/bin/env python3
def check(func):
  def wrapper(*args):
    if args[0].ser is None: raise Exception(f"[-] Ser is <None>. Can't {str(func)}")
    func(*args)
  return wrapper

class Uart():
  def __init__(self, dev='/dev/ttyS0', baud=9600):
    self.ser = None
    self.DEV, self.BAUD = dev, baud
    self._setup()

  def _setup(self):
    import serial
    self.ser = serial.Serial(self.DEV, self.BAUD)
    print("[*] Uart Initialized")

  @check
  def close(self):
    self.ser.close()

  @check
  def recv(self, n=1):
    return self.ser.read().decode()

  @check
  def send(self, dat):
    if not isinstance(dat, bytes): dat = dat.encode()
    self.ser.write(dat)

  def test(self):
    self.send("Hello World")
    self.close()

if __name__ == "__main__":
  #--testing
  u = Uart()
  u.test()
