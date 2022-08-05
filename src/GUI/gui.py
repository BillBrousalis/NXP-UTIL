#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkFont


class Gui(tk.Tk):
  _TITLE = 'LINESCAN VISUALIZATION'
  _WIDTH = 700
  _HEIGHT = 500
  _FONT = tkFont.Font(family='Cascadia Code', size=10, weight='bold')
  _COLORS = {'white': '#e6e6e6',
            'black': '#0f0f0f',
            'grey': '#707070'
  }
  def __init__(self):
    super().__init__()
    self.title(self._TITLE)
    self.draw_gui()

  def draw_gui(self):
    self.canvas = tk.Canvas(self, width=self._WIDTH, height=self._HEIGHT)
    self.canvas.pack()
    self.draw_graph()

  def draw_graph(self):
    self.graphcanvas = tk.Canvas(self.canvas, bg=self._COLORS['grey'], relief='groove')
    self.graphcanvas.place(anchor='n', relx=0.33, rely=0, relwidth=0.65, relheight=1)


  def exit(self):
    self.quit()
    self.destroy()

#--setup
def spawn_gui():
  g = Gui()
  g.resizable(False, False)
  g.protocol('WM_DELETE_WINDOW', g.exit)
  g.mainloop()

if __name__ == '__main__':
  print('[*] Spawning GUI Instance')
  spawn_gui()