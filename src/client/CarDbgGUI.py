#!/usr/bin/env python3
#=============================================================================
# Name        : CarDbgGUI
# Author      : Basilis Mprousalis
# Version     : 0.1
# Year        : 2022
# Description : Graphical User Interface For LineScan Camera Data Visualization
#==============================================================================
import os
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# MODULES
import client
import processing

# Get base dir of repo
def get_base_dir():
  import pathlib
  for p in pathlib.Path(__file__).parents:
    if os.path.basename(p) == 'NXP-UTIL': return p
  raise Exception("[-] Can't find base repository directory (Looking for NXP-UTIL).")

def get_config():
  import yaml
  with open(os.path.join(get_base_dir(), 'config/config.yaml'), 'r') as f:
    return yaml.safe_load(f)

# Threads to keep GUI running smoothly
# while updating values displayed
def threadexec(func):
  def wrapper(*args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    return t
  return wrapper

class Gui(tk.Tk):
  _TITLE = 'LINESCAN DATA VISUALIZATION'
  # Gui dims in px
  _WIDTH = 700
  _HEIGHT = 500
  _COLORS = {'white': '#fafafa',
            'black': '#0f0f0f',
            'grey': '#707070',
            'light blue': '#e6f7f7'
  }
  # Top-left icon
  _ICON = os.path.join(get_base_dir(), 'assets/icon.ico')
  _CONFIG = get_config()
  def __init__(self):
    print('[*] MAKE SURE SERVER IS RUNNING FIRST [*]')
    super().__init__()
    self.title(self._TITLE)
    self.iconbitmap(self._ICON)     # REMOVE LINE IF RUNNING /BUILDING ON LINUX
    self._FONT = tkFont.Font(family='Cascadia Code', size=13, weight='bold')
    self._FONTSMALL = tkFont.Font(family='Cascadia Code', size=10, weight='bold')
    self.draw_gui()
    # Data-specific
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
    steerlb.place(anchor='n', relx=0.8, rely=0.09, relwidth=0.225, relheight=0.05)
    # Steering value displayed
    self.steervallb = tk.Label(self.canvas, text='[ 0.0 ]', font=self._FONT, bg=self._COLORS['white'])
    self.steervallb.place(anchor='n', relx=0.85, rely=0.14, relwidth=0.225, relheight=0.05)
    # Horizontal separator
    hsep = ttk.Separator(self.canvas, orient='horizontal')
    hsep.place(relx=0.69, rely=0.218, relwidth=0.3, relheight=0.01)
    # "Speed" Label
    speedlb = tk.Label(self.canvas, text='Speed:', font=self._FONT, bg=self._COLORS['white'])
    speedlb.place(anchor='n', relx=0.738, rely=0.24, relwidth=0.1, relheight=0.05)
    # Speed value displayed
    self.speedvallb = tk.Label(self.canvas, text='[ 0.0 ]', font=self._FONT, bg=self._COLORS['white'])
    self.speedvallb.place(anchor='n', relx=0.85, rely=0.29, relwidth=0.225, relheight=0.05)
    # Start-Stop button
    self.but = tk.Button(self.canvas, text='START', font=self._FONT, bg=self._COLORS['white'], relief='groove', command=self.but_func)
    self.but.bind('<Enter>', lambda event, x=self.but : self.but_hover(x))
    self.but.bind('<Leave>', lambda event, x=self.but : self.but_hover_leave(x))
    self.but.place(anchor='n', relx=0.85, rely=0.03, relwidth=0.2, relheight=0.05)
    # Version label
    vers = tk.Label(self.canvas, text=f"[ v{self._CONFIG['VERSION']} ]", font=self._FONTSMALL, bg=self._COLORS['white'])
    vers.place(anchor='n', relx=0.95, rely=0.955, relwidth=0.09, relheight=0.04)

  def draw_graph(self):
    self.fig = plt.Figure()
    self.fig.set_facecolor(self._COLORS['white'])
    self.graphcanvas = FigureCanvasTkAgg(self.fig, master=self.canvas)
    self.graphcanvas.get_tk_widget().place(anchor='n', relx=0.34, rely=0.01, relwidth=0.67, relheight=0.98)
    self.ax = self.fig.add_subplot(111)
    self.ax.axis((0, 127, 0, 2))
    self.ax.set_title('--LineScan Readings--')
  
  def setup(self):
    self.DATA = {'LINE': [],
                 'STEER': 0,
                 'SPEED': 0
    }
    self.isrunning = False
    print('[*] Initializing client. Looking for running server...')
    self.client = client.Client()
    if self.client.sock is None: 
      while 1:
        self.client = client.Client()
        if self.client.sock is not None: break
    if self.client is None: raise Exception('[-] Client is <None>. Server not found.')

  # Update Gui steer / speed VALUE labels
  @threadexec
  def tUpdatelbs(self):
    while 1:
      if not self.isrunning: return
      # fetch and display new values
      #self.steervallb['text'] = 
      print('[ Thread ] tUpdatelbs()')

  # Read / store incoming data
  @threadexec
  def tReaddat(self):
    while 1:
      if not self.isrunning: return
      self.DATA['LINE'] = processing.decode(self.client.readbytes(n=self._CONFIG['BYTES-PER-LINE']), DEBUG=self._CONFIG['DEBUG'])
      assert(len(self.DATA['LINE']) == 128)
      # TODO: Implement
      #self.Data['STEER'] =
      #self.Data['SPEED'] =

  # Graphing
  @threadexec
  def tAnim(self):
    self.anim = FuncAnimation(self.fig, self.update_graph, interval=10)
    self.anim._start()
  
  def update_graph(self, i):
    if not self.isrunning: self.anim.event_source.stop()
    # clear previous graph
    self.ax.clear()
    if self._CONFIG['DEBUG']:
      # plot raw data
      self.ax.plot([i for i in range(128)], self.DATA['LINE'], color='blue', linewidth=3)
    else:
      datx, daty = processing.prep_graph_dat(self.DATA['LINE'])
      # plot new
      for gx, gy in zip(datx, daty): self.ax.plot(gx, gy, color='black', linewidth=8)

  # Start-Stop button functionality
  def but_func(self):
    if self.isrunning:
      self.isrunning = False
      self.but['text'] = 'START'
    else:
      self.isrunning = True
      # Start threads
      #self.tUpdatelbs()
      self.tReaddat()
      self.tAnim()
      self.but['text'] = 'STOP'

  # Visual - button highlight
  def but_hover(self, button, color=_COLORS['light blue']): button.configure(bg=color)
  def but_hover_leave(self, button, color=_COLORS['white']): button.configure(bg=color)

  def exit(self):
    print('[-] Exiting...')
    self.quit()
    self.destroy()

# spawn Gui instance
def spawn_gui():
  print('[*] Spawning GUI Instance')
  g = Gui()
  g.resizable(False, False)
  g.protocol('WM_DELETE_WINDOW', g.exit)
  g.mainloop()

if __name__ == '__main__':
  spawn_gui()