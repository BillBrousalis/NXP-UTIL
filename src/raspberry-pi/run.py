#!/usr/bin/env python3
import os
# MODULES
import algo
import uart
import server

# Get base dir of repo
def get_base_dir():
  import pathlib
  for p in pathlib.Path(os.path.abspath(__file__)).parents:
    if os.path.basename(p) == "NXP-UTIL": return p
  raise Exception("[-] Can't find base repository directory (Looking for NXP-UTIL).")

# Fetch config dict
def get_config()->dict:
  import yaml
  with open(os.path.join(get_base_dir(), "config/config.yaml"), "r") as f:
    return yaml.safe_load(f)

# Small custom argument parser
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
  config = get_config()
  dev, commands = argparser()
  if dev is None: dev = config['DEV']
  if commands is None: commands = config['COMMANDS']
  assert(dev >= 0 and dev < 5)
  print(f'[*] COMMANDS mode: {"**ON**" if commands else "**OFF**"}')
  print(f'[*] Expecting [ {dev} ] Client(s)')
  s = server.Server(port=config["RPI-PORT"], dev=dev)
  u = uart.Uart(uartdev=config['UART'], baud=config['UART-BAUD'])
  buf = None
  try:
    while 1:
      # Get Uart
      buf = u.recv(config['BYTES-TO-READ'])
      if config['DEBUG']: print(f'[ DEBUG ] UART Received:\n{buf}')
      # Pass buf to client(s) - commands to car
      if dev != 0: s.send(buf)
      elif commands: u.send(algo.custom(buf[:128], dbg=True))
      #TODO: deal with logging on rpi
      #if config['LOGGING'] == 'RPI':
  # basically Ctrl-C
  except KeyboardInterrupt:
    print('\n[-] Closing server & exiting...')
    s.close()
    u.close()
    exit()
  # generic exception
  except Exception as e:
    print(f'[-] Error: {e}')
    exit()

if __name__ == '__main__':
    print('[ Running RPI Loop ]')
    while 1: main()
