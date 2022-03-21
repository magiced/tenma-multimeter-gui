import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shelve

def get_path_to_open_file(
    title = "Open File...",
    types = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))
    ):

    """ opens a tkinter file open dialog, returns a Path object and saves
    the file open location so that next time you use the method, it starts in
    the same location so that you don't have to hunt through folders every time"""
    shelfFile = shelve.open('file_dialog_data')
    # try to open saved variables from shelfFile, if the saved variables are not there,
    # set the last open variable to "/"
    try:
        last_open_dir = shelfFile['last_open_dir']
    except KeyError:
        last_open_dir = "/"

    # open a tkinter file open dialog over all other windows
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    this_file =  Path(filedialog.askopenfilename(initialdir = last_open_dir,title = title, filetypes = types))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

def get_path_to_save_file(
        default_filename = '',
        title = "Save File...",
        types = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))
        ):
    """ opens a tkinter save file dialog, returns a Path object and saves
    the file open location so that next time you use the method, it starts in
    the same location so that you don't have to hunt through folders every time"""

    shelfFile = shelve.open('file_dialog_data')
    # try to open saved variables from shelfFile, if the saved variables are not there,
    # set the last open variable to "/"
    try:
        last_open_dir = shelfFile['last_open_dir']
    except KeyError:
        last_open_dir = "/"

    # open a tkinter file open dialog over all other windows
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    this_file =  Path(filedialog.asksaveasfilename(initialdir = last_open_dir,title = title, initialfile = default_filename, filetypes = types))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

def open_folder_path( title = "Open Folder..."):
    """ opens a tkinter file dialog, returns a Path object and saves
    the file open location so that next time you use the method, it starts in
    the same location so that you don't have to hunt through folders every time"""
    shelfFile = shelve.open('file_dialog_data')

    # try to open saved variables from shelfFile, if the saved variables are not there,
    # set the last open variable to "/"
    try:
        last_open_dir = shelfFile['last_open_dir']
    except KeyError:
        last_open_dir = "/"

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    this_file =  Path(filedialog.askdirectory(initialdir = last_open_dir,title = title))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

