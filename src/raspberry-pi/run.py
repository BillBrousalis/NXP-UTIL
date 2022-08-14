#!/usr/bin/env python3
import os
import math
# MODULES
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

def argparser():
  import sys
  dev, com = None, None
  if len(sys.argv) < 2: return (dev, com)
  for idx in range(1, len(sys.argv)):
    if sys.argv[idx] == '-h': 
      print('Optional Commands:\n'
            '   -h      Help\n\n'
            '--dev      specify expected number of clients\n'
            '           ex.     ./run.py --dev=3\n\n'
            '--com      enable COMMANDS mode\n'
            '           ex. --dev=0 --com\n')
      exit()
    elif '--dev=' in sys.argv[idx]: dev = int(sys.argv[idx].split('=')[1])
    elif '--com' in sys.argv[idx]: com = True
    else: raise Exception(f'Unknown argument: {sys.argv[idx]}')
  return (dev, com)

def main():
  testspeed, teststeer = 0, 0
  config = get_config()
  max_dev, commands = argparser()
  if max_dev is None: max_dev = config['MAX-DEV']
  if commands is None: commands = config['COMMANDS']
  assert(max_dev >= 0 and max_dev < 10)
  print(f'[*] COMMANDS mode: {"**ON**" if commands else "**OFF**"}')
  print(f'[*] Expecting [ {max_dev} ] Client(s)')
  s = server.Server(port=config["RPI-PORT"], max_dev=max_dev)
  u = uart.Uart(baud=config['UART-BAUD'])
  buf = None
  try:
    while 1: # mainloop
      if max_dev != 0:
        buf = u.recv(config['BYTES-PER-LINE'])
        if config['DEBUG']: print(f'[ DEBUG ] UART Received:\n{buf}')
        # Pass buf to client(s)
        s.send(buf)
      else: # COMMANDS unavailable while also having clients present TODO: have separate uart conn for data sending
        if commands:
          # Test
          testspeed += 0.0005
          teststeer += 0.005
          if testspeed > 30: testspeed = 25
          if teststeer > 60: teststeer = -60
          print(teststeer)
          x = testspeed if testspeed > 0 else 255+testspeed
          x = math.floor(x).to_bytes(1, 'little')
          y = teststeer if teststeer > 0 else 255+teststeer
          y = math.floor(y).to_bytes(1, 'little')
          u.send(x)
          u.send(y)
      '''
      if config['LOGGING'] == 'RPI':
        #TODO: deal with logging on rpi
        pass
      '''
  except KeyboardInterrupt:
    print('\n[-] Closing server & exiting...')
    s.close()
    exit()
  except Exception as e:
    print(f'[-] Error: {e}')

if __name__ == '__main__':
    while 1: main()
