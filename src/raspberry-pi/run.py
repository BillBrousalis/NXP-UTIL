#!/usr/bin/env python3
import os

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
  dev, com, dbg, port = None, None, None, None
  if len(sys.argv) < 2: return (dev, com, dbg, port)
  for idx in range(1, len(sys.argv)):
    if sys.argv[idx] in ('-h', '--help'): 
      print('\nOptional:\n\n'
            ' --help     Show Argument Options\n\n'
            ' --dev      specify expected number of clients\n'
            '            ex.    ./run.py --dev=3\n\n'
            ' --com      enable COMMANDS mode\n'
            '            ex.    ./rpi-run --dev=0 --com\n\n'
            ' --dbg      enable DEBUG mode\n'
            '            ex.    ./rpi-run --dev=1 --dbg\n\n'
            ' --port     specify connection port\n'
            '            ex ./rpi-run --port=9002\n\n')
      exit()
    elif '--dev=' in sys.argv[idx]: dev = int(sys.argv[idx].split('=')[1])
    elif '--com' in sys.argv[idx]: com = True
    elif '--dbg' in sys.argv[idx]: dbg = True
    elif '--port=' in sys.argv[idx]: port = int(sys.argv[idx].split('=')[1])
    else: raise Exception(f'Unknown argument: {sys.argv[idx]}')
  return dev, com, dbg, port

def main():
  dev, commands, dbg, port = argparser()
  # MODULES
  import algo
  import uart
  import server
  config = get_config()
  if dev is None: dev = config['DEV']
  if commands is None: commands = config['COMMANDS']
  if dbg is None: dbg = config['DEBUG']
  if port is None: port = config['RPI-PORT']
  assert(dev >= 0 and dev < 5)
  print('----')
  print(f'[*] COMMANDS mode: {"**ON**" if commands else "**OFF**"}')
  print(f'[*] DEBUG mode: {"**ON**" if dbg else "**OFF**"}')
  print(f'[*] Expecting [ {dev} ] Client(s)')
  print(f'[*] Running on port [ {port} ]')
  print('----')
  if dev is not None: s = server.Server(port=port, dev=dev)
  u = uart.Uart(uartdev=config['UART'], baud=config['UART-BAUD'])
  buf = None
  try:
    while 1:
      # Get Uart Data
      buf = u.recv(config['BYTES-TO-READ'])
      if dbg: print(f'[ DEBUG ] UART Received:\n{buf}')
      # Pass buf to client(s) - commands to car
      if dev != 0: s.send(buf)
      if commands: u.send(algo.custom(buf[:128], dbg=True))
      #TODO: deal with logging on rpi
      #if config['LOGGING'] == 'RPI':
  # Ctrl-C
  except KeyboardInterrupt:
    print('\n[-] Closing server & exiting...')
    s.close()
    u.close()
    exit()
  # generic exception
  except Exception as e:
    print(f'[-] Error: {e}')

if __name__ == '__main__':
    print('[ Running RPI Loop ]')
    while 1: main()
