#!/usr/bin/env python3
import uart
import server

def get_config():
  import os
  import yaml
  # run symlink to get path right
  with open("config/config.yaml", "r") as f:
    return yaml.safe_load(f)

def main():
  config = get_config()
  s = server.Server(port=config["RPI-PORT"], max_dev=config["MAX-DEV"])
  u = uart.Uart()
  buf = "Hello World" #init with None when ready
  try:
    while 1: # mainloop
      #TODO: implement uart.py 
      #buf = read uart bytes
      s.send(buf)
      if config["COMMANDS"]:
        #TODO: deal with commands
        pass
      if config["LOGGING"] == "RPI":
        #TODO: deal with logging on rpi
        pass
  except KeyboardInterrupt:
    print("\n[-] Closing server & exiting...")
    s.close()
    exit()
  except Exception as e:
    print(f"[-] Error: {e}")

if __name__ == "__main__":
  main()
