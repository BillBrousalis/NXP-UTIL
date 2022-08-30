#!/usr/bin/env python3
from simple_pid import PID
from scipy.signal import find_peaks
import time

# PID Params - Tune
KP, KD, KI = (1, 0, 0)
target = 0
pid = PID(KP, KD, KI, setpoint=target)
# Keep history of errors
# TODO: Support multiple entries
prev = 0

# prep data to be passed to uint8_t buffer
# speed / steer range (-100, 100) so it fits
def prep(x: int)->bytes: return (x if x > 0 else x+0x100).to_bytes(1, 'little')

# ** Develop custom algorithm here **
def custom(dat: list, dbg: bool)->int:
  # TODO: fix this please
  return prep(round(35))
  '''
  global prev
  err = processdata(dat)
  if err is None: err = prev
  steering_angle = pid(err)
  prev = err
  if dbg: printdbg(err, steering_angle)
  return prep(round(steering_angle))
  '''

# ** Process linescan data **
def processdata(dat: list, MAXVAL=64)->float:
  # TODO: fix "edge" case where one line is seen
  # flip peaks / valleys
  dat = [MAXVAL-x for x in dat]
  peaks = [x for x in find_peaks(dat, distance=10, prominence=12)[0]]
  if len(peaks) != 2: return None
  err = (((peaks[0] + peaks[1]) / 2) - 64) / 64
  print(f'>>>> {err}')
  return err


def printdbg(err, steer):
  print('--------------------------\n'
        f'[*]    ERROR VALUE: {err}\n'
        f'[*] STEERING ANGLE: {steer}\n')

if __name__ == '__main__':
  print('[ Running algorithm dummy set ]')
  dummydat = [0 for _ in range(128)]
  custom(dummydat)
elif __name__ == 'algo':
  print('[+] ALGO module added')
