#!/usr/bin/env python3

def decode(dat):
  # decode when 16 bytes are being send instead of 128
  return dat

# prep data into multi-part graph
def prep_graph_dat(dat):
  colors = {'white': 1, 'black': 2}
  draw = colors['white']
  # dat: array of ints 0 / 1
  y, x = [], []
  tmpy, tmpx = [], []
  prev = None
  for idx, val in enumerate(dat):
    if val != draw or idx == len(dat)-1:
      if prev == draw:
        if len(tmpy): y.append(tmpy)
        if len(tmpx): x.append(tmpx)
      tmpy, tmpx = [], []
      continue
    tmpy.append(val)
    tmpx.append(idx)
    prev = val
  return (x, y)