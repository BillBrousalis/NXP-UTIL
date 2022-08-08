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

def argparser():
  import sys
  if len(sys.argv) < 2: return None
  if sys.argv[1] == '-h': 
    print('Optional Commands:\n'
          '   -h      Help\n'
          '--dev      specify expected number of clients\n'
          '   ex.     ./run.py --dev=3\n')
    exit()
  elif '--dev=' in sys.argv[1]: return int(sys.argv[1].split('=')[1])
  else: raise Exception(f'Unknown argument: {sys.argv[1]}')

def main():
  config = get_config()
  max_dev = argparser()
  if max_dev is None: max_dev = config['MAX-DEV']
  assert(max_dev > 0 and max_dev < 10)
  print(f'[*] Expecting [ {max_dev} ] Client(s)')
  s = server.Server(port=config["RPI-PORT"], max_dev=max_dev)
  u = uart.Uart(baud=config['UART-BAUD'])
  buf = None
  try:
    while 1: # mainloop
      buf = u.recv(config['BYTES-PER-LINE'])
      print(f'[ DEBUG ] UART Received:\n{buf}')
      # Pass buf to clients
      s.send(buf)
      '''
      if config['COMMANDS']:
        #TODO: deal with commands
        pass
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
  main()
