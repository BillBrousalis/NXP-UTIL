#!/usr/bin/env python3
import os
##### MODULES #####
import uart
import server

def get_base_dir():
  import pathlib
  for p in pathlib.Path(__file__).parents:
    if os.path.basename(p) == "NXP-UTIL": return p
  raise Exception("[-] Can't find base repository directory (Looking for NXP-UTIL).")

def get_config():
  import yaml
  with open(os.path.join(get_base_dir(), "config/config.yaml"), "r") as f:
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
      # Until its actually written
      break
  except KeyboardInterrupt:
    print("\n[-] Closing server & exiting...")
    s.close()
    exit()
  except Exception as e:
    print(f"[-] Error: {e}")

if __name__ == "__main__":
  main()
