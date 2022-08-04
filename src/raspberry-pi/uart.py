#!/usr/bin/env python3

class Uart():
  def __init__(self):
    self._setup()

  def _setup(self):
    pass

  def recv(self, n=1):
    pass

  def send(self, dat):
    pass

  def test(self):
    pass

if __name__ == "__main__":
  #--testing
  u = Uart()
  u.test()
