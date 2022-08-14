#!/usr/bin/env python3
from simple_pid import PID

# PID Params - Tune
KP, KD, KI = (0, 0, 0)
target = 0
pid = PID(KP, KD, KI, setpoint=target)
# Keep history of errors
# TODO: Support multiple entries
prev = 0

# prep data to be passed to uint8_t buffer
# speed / steer range (-100, 100) so it fits
def prep(x: int)->bytes: return (x if x > 0 else x+255).to_bytes(1, 'little')

# develop custom algorithm here
def custom(dat: list, dbg: bool)->int:
  err = processdata(dat)
  steering_angle = pid(err)
  prev = err
  if dbg: printdbg(err, steering_angle)
  return prep(round(steering_angle))

# process linescan data
def processdata(dat: list)->float:
  return 0

def printdbg(err, steer):
  print('--------------------------\n'
        f'[*]    ERROR VALUE: {err}\n'
        f'[*] STEERING ANGLE: {steer}\n')

if __name__ == '__main__':
  print('[ Running dummy set ]')
  dummydat = [0 for _ in range(128)]
  custom(dummydat)
elif __name__ == 'algo':
  print('[+] ALGO module imported')