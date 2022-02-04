import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import time
import shelve
from pathlib import Path
import traceback

b_logging = True

def get_datetime_string():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def create_default_filename(string_in=''):
    return f"{get_datetime_string()}{string_in}.csv"

def get_file_save_name_with_tkinter(default_filename=""):
    shelfFile = shelve.open('mydata')

    # try to open saved variables from shelfFile, if the saved variables are not there,
    # set the last open variable to "/"
    try:
        last_open_dir = shelfFile['last_open_dir']
    except KeyError:
        last_open_dir = "/"

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    this_file =  Path(filedialog.asksaveasfilename(initialdir = last_open_dir, initialfile = default_filename, title = "Save log file",filetypes = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

def create_log_file():
    log_filename = get_file_save_name_with_tkinter(create_default_filename())
    out_text = f"Saving logfile as {log_filename}..."
    # textbox.insert('end',out_text + '\n')
    print(out_text)

    try:
        with open(log_filename, 'w', encoding="utf-8") as logfile:
            logfile.write('')
    except:
        print("Write fail")
        print(f"log_filename: {log_filename}")
        print(traceback.format_esc())
        quit()
    
    return log_filename

def write_header_to_log(log_filename, header_string):
    write_line_to_log(log_filename, header_string)    

def stop_log(log_filename):
    out_text = f"Logging Stopped"
    print(out_text)
    log_filename = None
    # textbox.insert('end',out_text + '\n')
    return None

def write_line_to_log(log_filename, line_string):
    try:
        with open(log_filename, 'a', encoding="utf-8") as logfile:
            logfile.write(line_string + '\n')
    except:
        print("Write fail")
        print(f"log_filename: {log_filename}")
        print(f"line_string: {line_string}")
        print(traceback.format_esc())
        quit()

header = "x,y,z"

this_log = None

this_log = create_log_file()
write_header_to_log(this_log,header)
write_line_to_log(this_log,"1,2,3")
write_line_to_log(this_log,"4,5,6")
stop_log(this_log)

this_log = create_log_file()
write_header_to_log(this_log,header)
write_line_to_log(this_log,"1,2,3")
write_line_to_log(this_log,"4,5,6")
stop_log(this_log)


