#GUI file generated by GUI Pie, developed by Jabberwock
#https://apps.microsoft.com/store/detail/gui-pie/9P5TH15LZSL7


import os
import sys
import subprocess
import math
from tkinter import *
from tkinter import ttk
import tkinter.font
try:
  from PIL import ImageTk, Image, ImageOps
except:
  print('Installing PIL.')
  subprocess.check_call(['pip', 'install', 'pillow'])
  print('Done.')
  from PIL import ImageTk, Image, ImageOps
dpiError = False
try:
  from ctypes import windll
  windll.shcore.SetProcessDpiAwareness(1)
except:
  print('ERROR. Could not set DPI awareness.')
  dpiError = True
if __name__ == "__main__":
  gui = Tk()
else:
  gui = Tk()
gui.title('ChainMed')
if dpiError:
  dpi = 96
else:
  dpi = gui.winfo_fpixels('1i')
gui.geometry(f'{math.ceil(400 * dpi / 96)}x{math.ceil(400 * dpi / 96)}')
gui.grid_propagate(False)
for x in range(30):
  Grid.columnconfigure(gui, x, weight=1, uniform='row')
  Label(gui, width = 1, bg = '#FFFFFF').grid(row = 0, column = x, sticky = N+S+E+W)
for y in range(30):
  Grid.rowconfigure(gui, y, weight=1, uniform='row')
  Label(gui, width = 1, bg = '#FFFFFF').grid(row = y, column = 0, sticky = N+S+E+W)
gui.configure(background='#FFFFFF')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~WIDGETS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
image_path = os.path.join(os.getcwd(),'Python dApp','image.jpg')
gui.BackgroundImageOriginal = Image.open(image_path.replace("\\","/"))
gui.BackgroundImageImage = ImageOps.exif_transpose(gui.BackgroundImageOriginal)
gui.BackgroundImageImage = ImageTk.PhotoImage(gui.BackgroundImageImage.resize((math.ceil(400 * dpi / 96), math.ceil(400 * dpi / 96)), Image.Resampling.LANCZOS))
gui.BackgroundImage = Label(gui, image = gui.BackgroundImageImage, width = 1, height = 1, bg = '#FFFFFF')
gui.BackgroundImage.grid(row = 0, column = 0, columnspan = 30, rowspan = 30, sticky = N+S+E+W)
gui.ModeLabel = Label(gui, text = "Mode:", font = ('Calibri', 16), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.ModeLabel.grid(row = 5, column = 3, columnspan = 10, rowspan = 2, sticky = N+S+E+W)
gui.PatientAddress = Label(gui, text = "Patient Address:", font = ('Calibri', 16), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.PatientAddress.grid(row = 8, column = 3, columnspan = 11, rowspan = 2, sticky = N+S+E+W)
gui.DoctorAddress = Label(gui, text = "Doctor Address:", font = ('Calibri', 16), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.DoctorAddress.grid(row = 11, column = 3, columnspan = 11, rowspan = 3, sticky = N+S+E+W)
gui.FilesAllowed = Label(gui, text = "Files allowed:", font = ('Calibri', 16), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.FilesAllowed.grid(row = 15, column = 3, columnspan = 11, rowspan = 2, sticky = N+S+E+W)
gui.FileUpload = Label(gui, text = "File to upload:", font = ('Calibri', 16), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.FileUpload.grid(row = 18, column = 3, columnspan = 12, rowspan = 2, sticky = N+S+E+W)
gui.WelcomeLabel = Label(gui, text = "Welcome to ChainMed!", font = ('Cambria', 20), width = 1, height = 1, fg = '#FFFFFF', bg = '#1BA1E2')
gui.WelcomeLabel.grid(row = 0, column = 3, columnspan = 25, rowspan = 3, sticky = N+S+E+W)
gui.Entry1 = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.Entry1.grid(row = 9, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.Entry1.insert(0, "")
gui.Entry2 = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.Entry2.grid(row = 12, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.Entry2.insert(0, "")
gui.Entry3 = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.Entry3.grid(row = 15, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.Entry3.insert(0, "")
gui.Entry4 = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.Entry4.grid(row = 18, column = 17, columnspan = 8, rowspan = 2, sticky = N+S+E+W)
gui.Entry4.insert(0, "")
def defocus(event):
  event.widget.master.focus_set()
gui.Dropdown1 = ttk.Combobox(gui, values = ['Set Files allowed','Upload File','Retrieve File',], width = 1, state = 'readonly')
gui.Dropdown1.grid(row = 5, column = 17, columnspan = 8, rowspan = 2, sticky = N+S+E+W)
gui.Dropdown1.bind('<FocusIn>', defocus)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BUTTONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def runSubmitEvent(argument):
  if not(__name__ == '__main__'):
    from main import SubmitEvent
    try:
      SubmitEvent(argument)
    except TypeError:
      SubmitEvent()
gui.SubmitButton = Button(gui, text = "Submit", font = ('DejaVu Sans', 16), width = 1, height = 1, fg = '#000000', command = lambda: runSubmitEvent("SubmitButton"), bg = '#F8CECC')
gui.SubmitButton.grid(row = 23, column = 11, columnspan = 6, rowspan = 3, sticky = N+S+E+W)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~HELPER FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initModules():
  raise Exception('This main file is outdated. Script main.py must be updated to reflect the changes in GUI Pie v3.')
def init():
  from main import SubmitEvent
gui.initModules = initModules
def hide():
  gui.withdraw()
def show():
  gui.deiconify()
def hideAllWidgets():
    gui.ModeLabel.grid_remove()
    gui.PatientAddress.grid_remove()
    gui.DoctorAddress.grid_remove()
    gui.FilesAllowed.grid_remove()
    gui.FileUpload.grid_remove()
    gui.WelcomeLabel.grid_remove()
    gui.Entry1.grid_remove()
    gui.Entry2.grid_remove()
    gui.Entry3.grid_remove()
    gui.Entry4.grid_remove()
    gui.SubmitButton.grid_remove()
    gui.Dropdown1.grid_remove()
gui.hideAllWidgets = hideAllWidgets
def showAllWidgets():
    gui.ModeLabel.grid()
    gui.PatientAddress.grid()
    gui.DoctorAddress.grid()
    gui.FilesAllowed.grid()
    gui.FileUpload.grid()
    gui.WelcomeLabel.grid()
    gui.Entry1.grid()
    gui.Entry2.grid()
    gui.Entry3.grid()
    gui.Entry4.grid()
    gui.SubmitButton.grid()
    gui.Dropdown1.grid()
gui.showAllWidgets = showAllWidgets
def run():
  global dimensions
  dimensions = [0,0]
  if __name__ != "__main__":
    init()
  resizeEvent(None)
  gui.mainloop()
gui.run = run
gui.hide = hide
gui.show = show

dimensions = [gui.winfo_width(), gui.winfo_height()]
def resize():
  global gui, dimensions
  if gui.winfo_width() != dimensions[0] or gui.winfo_height() != dimensions[1]:
    gui.ModeLabel.config(wraplength = math.ceil(gui.winfo_width() * 10 / 30) + 2)
    gui.PatientAddress.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    gui.DoctorAddress.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    gui.FilesAllowed.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    gui.FileUpload.config(wraplength = math.ceil(gui.winfo_width() * 12 / 30) + 2)
    gui.WelcomeLabel.config(wraplength = math.ceil(gui.winfo_width() * 25 / 30) + 2)
    gui.SubmitButton.config(wraplength = math.ceil(gui.winfo_width() * 6 / 30) + 2)
    gui.BackgroundImageOriginal = Image.open(r'C:/Users/User/Downloads/Untitled Diagram.jpg')
    gui.BackgroundImageImage = ImageOps.exif_transpose(gui.BackgroundImageOriginal)
    gui.BackgroundImageImage = ImageTk.PhotoImage(gui.BackgroundImageImage.resize((gui.winfo_width(), gui.winfo_height()), Image.Resampling.LANCZOS))
    gui.BackgroundImage.config(image = gui.BackgroundImageImage)
    dimensions = [gui.winfo_width(), gui.winfo_height()]

eventID = None
gui.resizeDelay = 100
def resizeEvent(event):
  global eventID
  if eventID:
    gui.after_cancel(eventID)
  eventID = gui.after(gui.resizeDelay, resize)
gui.bind('<Configure>', resizeEvent)
if __name__ == "__main__":
  gui.run()
