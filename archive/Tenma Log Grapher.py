try:
    import pandas as pd
except:
    print("This script requires the pandas library\nInstall it using the 'pip install pandas' command")
    quit()

try:
    import matplotlib.pyplot as plt
except:
    print("This script requires the matplotlib library\nInstall it using the 'pip install matplotlib' command")
    quit()

import os
import datetime as dt
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shelve
import datetime

def get_timestamp_from_string(string):
    return dt.datetime.fromisoformat(string)

def get_file_open_name_with_tkinter():
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
    this_file =  Path(filedialog.askopenfilename(initialdir = last_open_dir,title = "Select file",filetypes = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

### ========== PROGRAM ========== ###

filename = get_file_open_name_with_tkinter()
#TODO - if nothing gets picked, or cancel pressed, stop cell

print (f"Opening {filename.name}...")

if ((filename.suffix == ".csv")):
    df = pd.read_csv(filename, index_col = False)
else:
    print("ERROR - This script only works with csv files")
    print("Quitting...")
    quit()
    
print()
print("==== PLOTTING ====")

# add check to make sure mode is the same all the way through the log

df["datetime"] = df["Time"].apply(get_timestamp_from_string)

series_label = df.loc[1,'Mode']
y_label = f'[ {df.loc[1, "Actual Unit"]} ]'

fig, ax = plt.subplots(dpi=200)

ax.plot(df['datetime'],df['Actual Value'], label=series_label)

ax.set_title(filename.stem)
ax.set_xlabel("Time")
ax.set_ylabel(y_label)
plt.xticks(rotation=30, ha='right')  
          
fig.legend()
fig.show()

plt.savefig(filename.parent / (filename.stem +  '-GRAPH.png'),dpi=200)