#!/usr/bin/env python3
THRESHOLD = 120
def decode(dat, DEBUG=False):
  # decode when 16 bytes are being send instead of 128
  # TODO: implement 16-byte into 128 bit dec
  if DEBUG: 
    print(f'DATA:\n{[x for x in dat]}')
    return [int(x) for x in dat]
  return [1 if b > THRESHOLD else 0 for b in dat]

# prep data into multi-part graph
def prep_graph_dat(dat):
  # 1 to draw white parts of road
  # 0 to draw black parts
  draw = 1
  x, y = [], []
  tmpx, tmpy = [], []
  prev = None
  # Break into sections; Can't draw disconnected graph
  for idx, val in enumerate(dat):
    if val != draw or idx == len(dat)-1:
      if prev == draw:
        if len(tmpx): x.append(tmpx)
        if len(tmpy): y.append(tmpy)
      tmpy, tmpx = [], []
      continue
    tmpy.append(val)
    tmpx.append(idx)
    prev = val
  # x, y -> list of lists: plot each sublist ex. (x[0], y[0])
  return (x, y)