#!/usr/bin/env python3
import time
import random
import uart

if __name__ == '__main__':
  u = uart.Uart(dev='COM5', baud=115200)
  while 1:
    # increased odds of seeing 'white'
    rdat = [random.choice([b'0', b'1', b'1']) for _ in range(128)]
    u.send(b''.join(rdat)+b'\n')
    time.sleep(0.01)
