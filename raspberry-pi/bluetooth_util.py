#!/usr/bin/env python3
import bluetooth

class PiBT():
  def __init__(self):
    self.connected = False
    self.targetname = "BILL-LAPTOP"
    self.target = None
    self.port = 1
    self._setup()

  def __str__(self):
    dev = "\n".join([f"{name:>40}:  {mac}" for name,mac in self.get_available_devices().items()])
    return (f"Status: {'CONNECTED' if self.connected else 'NOT CONNECTED'}\n"
            f"Devices Avalailable:\n{dev}")

  def _setup(self):
    dev = self.get_available_devices()
    if self.targetname not in dev.keys(): raise Exception("Target Device not available")
    self.target = dev[self.targetname]
    self.connect()

  def connect(self, target=None, port=None):
    if target is None: target = self.target
    if port is None: port = self.port
    if self.connected: raise Exception("Already connected to a device")
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target, port))
    self.connected = True

  def get_available_devices(self):
    dev = bluetooth.discover_devices()
    names = [bluetooth.lookup_name(x) for x in dev]
    return {key:val for (key, val) in zip(names, dev)}

  def test(self):
    if not self.connected: raise Exception("Not connected to a device")
    sock.send(b"Hello World!\n")
    sock.close()
    self.connected = False

if __name__ == '__main__':
  #-- testing
  bt = PiBT()
  bt.test()
