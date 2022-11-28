
import os
import sys
from web3 import Web3
import os
from deploy import retrieve_file,upload_file,set_file_allowed
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv
from hashlib import sha256
import subprocess
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font
from tkinter import filedialog
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
gui.geometry(f'{math.ceil(600 * dpi / 96)}x{math.ceil(600 * dpi / 96)}')
gui.grid_propagate(False)
for x in range(30):
  Grid.columnconfigure(gui, x, weight=1, uniform='row')
  Label(gui, width = 1, bg = '#FFFFFF').grid(row = 0, column = x, sticky = N+S+E+W)
for y in range(30):
  Grid.rowconfigure(gui, y, weight=1, uniform='row')
  Label(gui, width = 1, bg = '#FFFFFF').grid(row = y, column = 0, sticky = N+S+E+W)
gui.configure(background='#FFFFFF')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~WIDGETS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
image_path = os.path.join(os.getcwd(),'dApp','image.jpg')
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
gui.PatientAddress = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.PatientAddress.grid(row = 9, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.PatientAddress.insert(0, "")
gui.DoctorAddress = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.DoctorAddress.grid(row = 12, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.DoctorAddress.insert(0, "")
gui.FilesAllowed = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.FilesAllowed.grid(row = 15, column = 17, columnspan = 8, rowspan = 1, sticky = N+S+E+W)
gui.FilesAllowed.insert(0, "")
gui.FileUpload = Entry(gui, width = 1, bg = '#FFFFFF', font = ('Arial', 16), justify = 'center', highlightthickness = 0, bd=0)
gui.FileUpload.grid(row = 18, column = 17, columnspan = 8, rowspan = 2, sticky = N+S+E+W)
gui.FileUpload.insert(0, "")
def defocus(event):
  event.widget.master.focus_set()
gui.Mode = ttk.Combobox(gui, values = ['Set Files allowed','Upload File','Retrieve File',], width = 1, state = 'readonly')
gui.Mode.grid(row = 5, column = 17, columnspan = 8, rowspan = 2, sticky = N+S+E+W)
gui.Mode.bind('<FocusIn>', defocus)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EXCEPTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AllowedFilesException(Exception):
    def __init__(self, message):
        super().__init__(message)
class MissingPatientException(Exception):
    def __init__(self, message):
        super().__init__(message)
class MissingDoctorException(Exception):
    def __init__(self, message):
        super().__init__(message)
class MissingFileException(Exception):
    def __init__(self, message):
        super().__init__(message)
class MissingFileNumberException(Exception):
    def __init__(self, message):
        super().__init__(message)
class TransactionException(Exception):
    def __init__(self, message):
        super().__init__(message)

def triggerException(patient,doctor,file,number,mode):
    if(patient == ""):
        raise MissingPatientException("Patient Address is missing!")
    elif(doctor == ""):
        raise MissingDoctorException("Doctor Address is missing!")
    if(mode == 'Set Files allowed'):
        if (number == ""):
            raise MissingFileNumberException("Please specify number of files allowed for this Patient!")
        elif(int(number) < 0):
            raise AllowedFilesException("Please input a reasonable file number!")
    elif(mode == 'Upload File'):
        if(file == ""):
            raise MissingFileException("Please select a file!")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BUTTONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Submit():
    
    # Fetching all the necessary parameters and storing in respective variables
    patientAddress = gui.PatientAddress.get()
    doctorAddress = gui.DoctorAddress.get()
    fileUpload = gui.FileUpload.get()
    fileAllowed = gui.FilesAllowed.get()
    mode = gui.Mode.get()
    load_dotenv()
    abi = os.getenv('ABI')
    Contract_address = os.getenv("Contract_Address")
    url = os.getenv('URL')
    host = os.getenv('IPFS_Host')
    rx_port = os.getenv('IPFS_RX_PORT')
    tx_port = os.getenv('IPFS_TX_PORT')

    try:
        triggerException(patientAddress,doctorAddress,fileUpload,fileAllowed,mode)
        patientAddress = Web3.toChecksumAddress(gui.PatientAddress.get())
        doctorAddress = Web3.toChecksumAddress(gui.DoctorAddress.get())
        if(mode == 'Set Files allowed'):
            
            fileAllowed = int(gui.FilesAllowed.get())
            tx = set_file_allowed(abi,url,doctorAddress,patientAddress,Contract_address,fileAllowed)
     

        elif(mode == 'Upload File'):
            
            fileUpload = fileUpload.replace("/","\\")
            tx = upload_file(abi,url,host,tx_port,fileUpload,doctorAddress,patientAddress,Contract_address)
            
        
        elif(mode == 'Retrieve File'):
            
            tx = retrieve_file(abi,url,host,rx_port,doctorAddress,patientAddress,Contract_address)
            

        messagebox.showinfo("Success",message="Transaction Successful!")


    except MissingPatientException as error:
        messagebox.showerror("Error",message=error)
    except MissingDoctorException as error:
        messagebox.showerror("Error",message=error)
    except MissingFileNumberException as error:
        messagebox.showerror("Error",message=error)
    except MissingFileException as error:
        messagebox.showerror("Error",message=error)
    except AllowedFilesException as error:
        messagebox.showerror("Error",message=error)
    except ContractLogicError as error:
        messagebox.showerror("Error",message=error)
def Browse():
    file = filedialog.askopenfile(parent=gui,mode='rb',title='Choose a file')
    gui.FileUpload.insert(0,file.name)
gui.SubmitButton = Button(gui, text = "Submit", font = ('DejaVu Sans', 16), width = 1, height = 1, fg = '#000000', command = Submit, bg = '#F8CECC')
gui.SubmitButton.grid(row = 23, column = 11, columnspan = 6, rowspan = 3, sticky = N+S+E+W)
gui.BrowseButton = Button(gui, text = "Browse", font = ('Calibri', 8), width = 1, height = 1, fg = '#000000', command = Browse, bg = '#F8CECC')
gui.BrowseButton.grid(row = 18, column = 26, columnspan = 3, rowspan = 2, sticky = N+S+E+W)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~HELPER FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def initModules():
  raise Exception('This main file is outdated. Script main.py must be updated to reflect the changes in GUI Pie v3.')
def init():
  from main import Submit
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
    gui.PatientAddress.grid_remove()
    gui.DoctorAddress.grid_remove()
    gui.FilesAllowed.grid_remove()
    gui.FileUpload.grid_remove()
    gui.SubmitButton.grid_remove()
    gui.BrowseButton.grid_remove()
    gui.Mode.grid_remove()
gui.hideAllWidgets = hideAllWidgets
def showAllWidgets():
    gui.ModeLabel.grid()
    gui.PatientAddress.grid()
    gui.DoctorAddress.grid()
    gui.FilesAllowed.grid()
    gui.FileUpload.grid()
    gui.WelcomeLabel.grid()
    gui.PatientAddress.grid()
    gui.DoctorAddress.grid()
    gui.FilesAllowed.grid()
    gui.FileUpload.grid()
    gui.SubmitButton.grid()
    gui.BrowseButton.grid()
    gui.Mode.grid()
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
    # gui.PatientAddress.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    # gui.DoctorAddress.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    # gui.FilesAllowed.config(wraplength = math.ceil(gui.winfo_width() * 11 / 30) + 2)
    # gui.FileUpload.config(wraplength = math.ceil(gui.winfo_width() * 12 / 30) + 2)
    gui.WelcomeLabel.config(wraplength = math.ceil(gui.winfo_width() * 25 / 30) + 2)
    gui.SubmitButton.config(wraplength = math.ceil(gui.winfo_width() * 6 / 30) + 2)
    gui.BrowseButton.config(wraplength = math.ceil(gui.winfo_width() * 6 / 30) + 2)
    gui.BackgroundImageOriginal = Image.open(image_path.replace("\\","/"))
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
