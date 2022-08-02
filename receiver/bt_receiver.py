#!/usr/bin/env python3
import bluetooth

class BtReceiver():
  def __init__(self):
    self.connected = False
    self.port = 1
    self.server_sock = None
    self.client = None
  
  def __str__(self):
    return f"State: {'CONNECTED' if self.connected else 'NOT CONNECTED'}"

  def accept(self):
    self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    self.server_sock.bind(("", self.port))
    self.server_sock.listen(1)
    self.client, addr = self.server_sock.accept()
    print(f"Accepted connection from: {self.client} , {addr}")
    print(f"RECEIVED: {self.client.recv(1024)}")

  def test(self):
    pass
    #if self.

if __name__ == "__main__":
  #-- testing
  bt = BtReceiver()
  print(bt)
  bt.accept()
