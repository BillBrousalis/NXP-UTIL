#!/usr/bin/env python3
# uart buffer is uint8_t type
# convert speed / steer to signed
def uint2int(n):
  if n < 0x7f: return n
  else: return (-(~n&0xff))

def decode(dat, DEBUG: bool, THRESHOLD=120):
  # decode when 16 bytes are being send instead of 128
  # TODO: implement 16-byte into 128 bit dec
  if DEBUG: 
    #print(f'DATA:\n{[x for x in dat]}')
    # data coming in: 0-127th byte -> line data, 128-129th byte -> speed / steer value
    return (list(dat[:128]), uint2int(dat[128]), uint2int(dat[129]), [uint2int(dat[130]), uint2int(dat[131])])
  return ([1 if b > THRESHOLD else 0 for b in dat[:128]], uint2int(dat[128]), uint2int(dat[129]))

# prep data into multi-part graph
def prep_graph_dat(dat: list):
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
  # x, y -> list of lists
  # plot each sublist ex. (x[0], y[0])
  return (x, y)

if __name__ == '__main__':
  print('[ Running prep_graph_dat Test ]')
  x = [0 for _ in range(30)] +\
      [1 for _ in range(30)] +\
      [0 for _ in range(40)] +\
      [1 for _ in range(18)]
  print(f'Input:\n{x}')
  print(f'Out:\n{prep_graph_dat(x)}')
elif __name__ == 'processing':
  print('[+] PROCESSING module added') 
