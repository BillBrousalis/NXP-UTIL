#!/usr/bin/env python3
import socket

class Server():
  def __init__(self):
    self.host, self.port = '', 9001 #socket.gethostname(), 9001
    print(self.host, self.port)
    self.test() 

  def test(self):
<<<<<<< HEAD
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 60001     # Port to listen on (non-privileged ports are > 1023)

=======
>>>>>>> 6e28d549f10380b4195dc217cb4334e2137bc6a5
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.host, self.port))
      s.listen(1)
      conn, addr = s.accept()
      with conn:
        print(f"Connected by {addr}")
        while True:
          data = conn.recv(1024)
          if not data:
            break
          conn.sendall(data)

if __name__ == "__main__":
  #--testing
  s = Server()
