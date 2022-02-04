# from logging import exception

import serial
import serial.tools.list_ports
import time
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog
# from os import path
import shelve
from pathlib import Path
import traceback
# import plotCSV

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tenma import *

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

########## Logging Functions ##########

def create_log_file(name_string = ''):
    log_filename = get_file_save_name_with_tkinter(create_default_filename(name_string))
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
        if log_filename != None:
            with open(log_filename, 'a', encoding="utf-8") as logfile:
                logfile.write(line_string + '\n')
    except:
        # note, this usually appears when b_logging is true, but the log_filename
        # hasn't bee returned by the file dialog yet (because of tkinter, this 
        # is kind of acting like threading)
        print("Write fail")
        print(f"log_filename: {log_filename}")
        print(f"line_string: {line_string}")
        print(traceback.format_esc())
        quit()

########## GUI functions ##########

def get_available_com_ports():
    print("Finding ports...")
    ports = serial.tools.list_ports.comports()
    return ports

def open_close_port():
    global b_ser_port_open
    if b_ser_port_open: # if port is open, close it
        # close port
        ser.close()
        write_to_textbox(f'Closed serial port {cbo_ports.get()}')
        b_ser_port_open = False
        btn_open['text'] = "CONNECT"
        # toggle_graphing()
    else:               # if port is closed, open it
        port = cbo_ports.get()
        # speed = cbo_speed.get()
        ser.close()
        ser.port = port
        # ser.baudrate = speed
        set_tenma_serial_settings()
        try:
            ser.open()
            write_to_textbox(f'Opened serial port {cbo_ports.get()}')
        except:
            write_to_textbox('ERROR: Failed to open serial port {0} at {1}'.format(cbo_ports.get(),cbo_speed.get()))
        b_ser_port_open = True
        btn_open['text'] = "DISCONNECT"
        start_graph()

        # toggle_graphing()

def write_to_textbox(instring):
    textbox.configure(state='normal')

    textbox.insert('end',instring + '\n')
    textbox.configure(state='disabled')
    textbox.see(tk.END)

def clear_textbox():
    textbox.delete(1.0,'end')

def send_serial():
    data = tx_text.get()
    try:
        ser.write(data.encode('utf-8'))
        textbox.insert('end','SEND: ' + data + '\n')
    except NameError:
        write_to_textbox('ERROR: No Serial Port Open!')

def toggle_lbl_rec_colour(b_rec):
    if b_rec:
        lbl_rec['bg'] = '#FFFFCC' #'blue'
    else:
        lbl_rec['bg'] = 'white'
    return not b_rec

def toggle_log():
    global b_logging
    global log_file
    if b_logging: #when logging is on

        b_logging = False
        btn_log['text'] = 'Start Log'
        # btn_log['bg'] = 'green'
        log_file = stop_log(log_file)
    else: # when not logging
        b_logging = True
        btn_log['text'] = 'Stop Log'
        # btn_log['bg'] = 'red'
        log_file = create_log_file('Tenma log')
        write_header_to_log(log_file,tenma_header)

def log_data(log_file, data_in):
    global b_logging
    if b_logging and (log_file != ''):
        data_line_string = get_log_line_from_tenma_message(data_in)
        write_line_to_log(log_file, data_line_string)

def get_log_line_from_tenma_message(msg_in):
    log_line = f"{msg_in['Time']},{msg_in['Mode']},{msg_in['OL']},{msg_in['Display Value']},{msg_in['Display Unit']},{msg_in['Actual Value']},{msg_in['Actual Unit']},{msg_in['AD/DC']},{msg_in['Reading Type']},{msg_in['Hold']},{msg_in['Meter State']},{msg_in['Bar Graph State']},{msg_in['Bar Graph Value']},{msg_in['Z1']},{msg_in['Z2']},{msg_in['Z3']},{msg_in['Z4']}"
    return log_line

def set_tenma_serial_settings():
    ser.baudrate = 2400
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 3
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = 3
    ser.setRTS(False) # required for tenma meters, as these lines power the optical reciever circuit
    ser.setDTR(True) 



def main_program_loop():
    global b_logging
    global last_b_logging
    global log_file
    global meter_msg
    global b_rec
    if ser.is_open:
        while ser.in_waiting > 0:
            data = ser.readline()#.decode('ascii').strip().split()
            b_rec = toggle_lbl_rec_colour(b_rec)
            # print(data)
            try:
                meter_msg = get_tenma_vals_from_ser_msg(data)
                # lbl_serial_rx['text'] = data
                if meter_msg['OL'] == True:
                    lbl_display_val['text'] = 'OL'
                else:
                    lbl_display_val['text'] = f"{meter_msg['Display Value']:.03f}{meter_msg['Display Unit']}"
                out_text = get_log_line_from_tenma_message(meter_msg)
                textbox.insert('end',out_text + '\n')
                # print(out_text)
            except:
                print(f"EXCEPTION! data read -> {data}")
                # pass # if we have a dodgy message, just skip it
            try:
                log_data(log_file, meter_msg)
            except:
                print(f"EXCEPTION! flogging -> {log_file} - meter_msg:{meter_msg}")

            # print(out_text)

    # last_b_logging = b_logging            
    window.after(10,main_program_loop) # run this every 10 milli seconds

########## GRAPH FUNCTIONS ##########

def fifo(list_in, new_val):
    del list_in[0] #delete first in value
    list_in.append(new_val) #append new value to end
    return list_in

def init():  # only required for blitting to give a clean slate.
    for i in range(len(fifo_list)):
        line0.set_ydata([np.nan] * len(x) )
    return line0,

def animate(i):
    global b_graph_active
    global fifo_list
    global meter_msg
    # this function updates the y data each time
    if b_graph_active:
        try:
            new_val = meter_msg['Actual Value'] #random.randint(2,50)
            fifo_list = fifo(fifo_list, new_val)
            ax.autoscale(tight=False)
            y_scale_max = max(fifo_list) * 1.1 # gives a 10% margin to let you see the line when it's at the top
            ax.set_ybound(lower = 0, upper = y_scale_max) # sets limits of y axis
        except KeyError:
            pass
    else:
        fifo_list = [0]*list_length

    # ax.set_yticks( )
    line0.set_ydata(fifo_list)
    return line0,

def clear_graph():
    global b_clear_list
    b_clear_list = True

def start_graph():
    global b_graph_active
    b_graph_active = True
    btn_graph_on['text'] = 'STOP GRAPH'

def toggle_graphing():
    global b_graph_active

    if b_graph_active: # if turning graph off
        b_graph_active = False
        btn_graph_on['text'] = 'START GRAPH'
    else: # if turning graph on
        b_graph_active = True
        btn_graph_on['text'] = 'STOP GRAPH'

def initialise_graph():
    fig, ax = plt.subplots()
    list_length = 30 # int(cbo_graph_width.get())

    #generate starting data
    fifo_list = [0]*list_length
    x = [i for i in range(list_length)]
    plots = []
    #create the figure
    # fig, ax = plt.subplots()

    line0, = ax.plot(x, fifo_list, label = 'Value', color="red")
    ax.set_ybound(lower = 0, upper = 20) # sets limits of y axis
    # fig.legend()

    return fig


""" DEFINE GUI WIDGETS """

window = tk.Tk()
window.title('Tenma 72-2610 Multimeter Interface')

cbo_ports = ttk.Combobox(window)
# this list comprehension takes the port objects in the list returned by the comports method
# and returns a list of their device names
# otherwise it populates the combo box with the description string which can't be used to 
# open the port
list_of_ports = [i.device for i in serial.tools.list_ports.comports()] #('/dev/ttyUSB0','/dev/ttyUSB1','COM17')
cbo_ports['value'] = list_of_ports
cbo_ports.current(0) # start the box on the first value in the list

#create the canvas
fig = initialise_graph()
canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
canvas.draw() # why is the canvas drawn here?

cbo_speed = ttk.Combobox(window)
cbo_speed['values'] = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)
cbo_speed.current(2)

lbl_graph_width = tk.Label(window, text='Graph time [s]', justify='left')
cbo_graph_width = ttk.Combobox(window)
cbo_graph_width['values'] = (60,300,600,3600)
cbo_graph_width.current(0)

btn_open = tk.Button(window, text='CONNECT',command=open_close_port)

textbox = tk.scrolledtext.ScrolledText(window, width=50, height=4)
btn_graph_on = tk.Button(window, text='START GRAPH', command=toggle_graphing)

tx_text = tk.Entry(window, width=30)
tx_text.focus()
btn_transmit = tk.Button(window, text='TRANSMIT', command=send_serial)
lbl_rec = tk.Label(window, text='MSG REC', bg='white', justify='center', relief='solid', borderwidth=2, padx=5, pady=5, font=('bold'))
btn_log = tk.Button(window, text='Start Log', command=toggle_log)

lbl_serial_rx = tk.Label(window, text='serial comes out here')

lbl_display_val = tk.Label(window, text='------', justify='left', font=('Arial',50,'bold'))

""" DEFINE GUI LAYOUT """
# row 0
cbo_ports.grid( row=0,  column=0)
cbo_speed.grid( row=0,  column=1)
btn_open.grid(  row=0,  column=2)

# row 1
lbl_rec.grid(       row=1,  column=0)
lbl_display_val.grid(row=1, column=1)#, columnspan=2)
btn_log.grid(       row=1,  column=2)

# row 2 
canvas.get_tk_widget().grid(row=2,  column=0, columnspan=3) # , side=tk.TOP, fill=tk.BOTH, expand=1) # Graph display

# row 3
#tx_text.grid(       row=3,  column=0,   columnspan=2)
#btn_transmit.grid(  row=3,  column=2)

# row 4
btn_graph_on.grid(  row=4,  column=0)
lbl_graph_width.grid(  row=4,  column=1)
cbo_graph_width.grid(  row=4,  column=2)

# row 5
# lbl_serial_rx.grid(         row=5, column=0,  sticky='e')

# row 6
textbox.grid(   row=6,  column=0,   columnspan=3)

### INITIALISATIONS ###



# this calls the animate function every 100ms
# https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=250, blit=False) #blit=True)

b_clear_list = False

messages_rec = []
msg_rec = bytearray()
rec_length = 0
num_reads = 30

list_length = 30

b_rec = False
b_reading = True
read_count = 0
tenma_header = f"Time,Mode,Display Value,Display Unit,Actual Value,Actual Unit,AD/DC,Reading Type,Hold,Meter State,Bar Graph State,Bar Graph Value,Z1,Z2,Z2,Z4"
b_ser_port_open = False
b_graph_active = False
b_logging = False
last_b_logging = False
log_file = None
meter_msg = {}
ser = serial.Serial()

main_program_loop()
window.mainloop()
