#!/usr/bin/env python3

def decode(dat):
  # decode when 16 bytes are being send instead of 128
  # TODO: implement 16-byte into 128 bit dec
  return list([int(x) for x in dat.decode()])

# prep data into multi-part graph
# TODO: there has to be a better way to write this
def prep_graph_dat(dat):
  colors = {'white': 1, 'black': 0}
  draw = colors['white']
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
  # x, y -> list of lists: plot each sublist ex. (x[0], y[0])
  return (x, y)