#!/usr/bin/env python3
#=============================================================================
# Name        : CarVisGUI
# Author      : Basilis Mprousalis
# Version     : 0.1
# Year        : 2022
# Description : Graphical User Interface For LineScan Camera Data Visualizatin
#==============================================================================
import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_base_dir():
  import pathlib
  for p in pathlib.Path(__file__).parents:
    if os.path.basename(p) == "NXP-UTIL": return p
  raise Exception("[-] Can't find base repository directory (Looking for NXP-UTIL).")

def get_config():
  import yaml
  with open(os.path.join(get_base_dir(), "config/config.yaml"), "r") as f:
    return yaml.safe_load(f)

def threadexec(func):
  def wrapper(*args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.start()
    return t
  return wrapper

class Gui(tk.Tk):
  _TITLE = 'LINESCAN VISUALIZATION'
  _WIDTH = 700
  _HEIGHT = 500
  _COLORS = {'white': '#fafafa',
            'black': '#0f0f0f',
            'grey': '#707070'
  }
  _CONFIG = get_config()
  def __init__(self):
    super().__init__()
    self.title(self._TITLE)
    self._FONT = tkFont.Font(family='Cascadia Code', size=13, weight='bold')
    self._FONTSMALL = tkFont.Font(family='Cascadia Code', size=10, weight='bold')
    self.draw_gui()
    self.setup()
  
  def draw_gui(self):
    self.canvas = tk.Canvas(self, width=self._WIDTH, height=self._HEIGHT, bg=self._COLORS['white'])
    self.canvas.pack()
    # Graph-specific
    self.draw_graph()
    # Vertical separator
    vsep = ttk.Separator(self.canvas, orient='vertical')
    vsep.place(relx=0.68, rely=0.015, relwidth=0.002, relheight=0.97)
    # "Steering Angle" Label
    steerlb = tk.Label(self.canvas, text='Steering Angle:', font=self._FONT, bg=self._COLORS['white'])
    steerlb.place(anchor='n', relx=0.8, rely=0.05, relwidth=0.225, relheight=0.05)
    # Steering value displayed
    steervallb = tk.Label(self.canvas, text='[ 0 ]', font=self._FONT, bg=self._COLORS['white'])
    steervallb.place(anchor='n', relx=0.85, rely=0.1, relwidth=0.225, relheight=0.05)
    # Horizontal separator
    hsep = ttk.Separator(self.canvas, orient='horizontal')
    hsep.place(relx=0.69, rely=0.178, relwidth=0.3, relheight=0.01)
    # "Speed" Label
    speedlb = tk.Label(self.canvas, text='Speed:', font=self._FONT, bg=self._COLORS['white'])
    speedlb.place(anchor='n', relx=0.738, rely=0.2, relwidth=0.1, relheight=0.05)
    # Speed value displayed
    speedvallb = tk.Label(self.canvas, text='[ 0 ]', font=self._FONT, bg=self._COLORS['white'])
    speedvallb.place(anchor='n', relx=0.85, rely=0.25, relwidth=0.225, relheight=0.05)
    # Version label
    vers = tk.Label(self.canvas, text=f"[ v{self._CONFIG['VERSION']} ]", font=self._FONTSMALL, bg=self._COLORS['white'])
    vers.place(anchor='n', relx=0.95, rely=0.955, relwidth=0.09, relheight=0.04)

  def draw_graph(self):
    self.fig = plt.Figure()
    self.fig.set_facecolor(self._COLORS['white'])
    self.graphcanvas = FigureCanvasTkAgg(self.fig, master=self.canvas)
    self.graphcanvas.get_tk_widget().place(anchor='n', relx=0.36, rely=0.01, relwidth=0.7, relheight=0.98)
    self.ax = self.fig.add_subplot(111)
    self.ax.grid()
    self.ax.set_title('LineScan Readings')
  
  def setup(self):
    self.DATA = {'LINE': [],
                 'STEER': 0,
                 'SPEED': 0
    }

  @threadexec
  def tUpdatelbs(self):
    import time
    time.sleep(10)
    pass
    
  @threadexec
  def tReaddat(self):
    pass

  @threadexec
  def tAnim(self):
    pass

  def exit(self):
    print("[-] Exiting...")
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