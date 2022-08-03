#!/usr/bin/env python3
import uart
import server

def main():

  n = 128
  buf = None
  try:
    loop() 
  except KeyboardInterrupt:
    print("\n[-] Closing server & exiting...")
    s.close()
    exit()
  except Exception as e:
    print(f"[-] Error: {e}")

  def loop:
    u = Uart()
    s = Server()
    while 1:
      buf = u.readbytes(n)

if __name__ == "__main__":
  main()
