#!/usr/bin/env python3
def test():
  colors = {"white": 1, "black": 2}
  dat = [colors["white"] for _ in range(20)] + \
        [colors["black"] for _ in range(10)] + \
        [colors["white"] for _ in range(70)] + \
        [colors["black"] for _ in range(10)] + \
        [colors["white"] for _ in range(18)]

  draw = colors["white"]
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

  import matplotlib.pyplot as plt
  for gy, gx in zip(y, x):
    plt.plot(gx, gy, color='black')
  plt.title("LineScan Visualizer")
  plt.axis((0, 127, 0, 2))
  plt.show()

if __name__ == "__main__":
  test()
