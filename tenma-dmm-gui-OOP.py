# from logging import exception

import serial
import serial.tools.list_ports
import time
import traceback
import datetime
import shelve
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

# my libraries
from easyfiledialogs import get_path_to_save_file
import tenma_interpreter
import tkgraph
import tkLED

def get_datetime_string():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def create_default_filename(string_in='', file_suffix='csv'):
    return f"{get_datetime_string()}{string_in}.{file_suffix}"

########## Logging Functions ##########

def create_log_file(name_string = ''):
    log_filename = get_path_to_save_file(default_filename = create_default_filename(name_string))
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

def get_list_of_available_com_ports():
    print("Finding ports...")
    ports = [i.device for i in serial.tools.list_ports.comports()]
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
        graph_width = int(cbo_graph_width.get())
        print(f'Graph Width: {graph_width}')
        # start_graph()

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
        log_file = create_log_file('')
        write_header_to_log(log_file,tenma_header)

def get_log_period():
    periods = {'natural', '30 secs', '1 minute', '5 mins', '10 mins'}

def log_data(log_file, data_in):
    global b_logging
    if b_logging and (log_file != ''):
        data_line_string = tenma.get_log_line_from_tenma_message(data_in)
        write_line_to_log(log_file, data_line_string)
        led_log.toggle()

# def get_log_line_from_tenma_message(msg_in):
#     log_line = f"{msg_in['Time']},{msg_in['Mode']},{msg_in['OL']},{msg_in['Display Value']},{msg_in['Display Unit']},{msg_in['Actual Value']},{msg_in['Actual Unit']},{msg_in['AD/DC']},{msg_in['Reading Type']},{msg_in['Hold']},{msg_in['Meter State']},{msg_in['Bar Graph State']},{msg_in['Bar Graph Value']},{msg_in['Z1']},{msg_in['Z2']},{msg_in['Z3']},{msg_in['Z4']}"
#     return log_line

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

# todo, oop this
# create tenma object
def main_program_loop():
    global b_logging
    global last_b_logging
    global log_file
    global meter_msg
    global b_rec
    global y_coords
    global x_coords
    global graph_width

    if ser.is_open:
        while ser.in_waiting > 0:
            data = ser.readline()#.decode('ascii').strip().split()
            led_rec.toggle()
            # print(data)
            try:
                meter_msg = tenma.interpret_tenma_722610_msg(data)

                if meter_msg['OL'] == True:
                    lbl_display_val['text'] = 'OL'
                else:
                    lbl_display_val['text'] = f"{meter_msg['Display Value']:.03f}{meter_msg['Display Unit']}"

                    # TODO, this should be added to the graph code instead
                    # should be y data only, or x should be elapsed time
                    # if y data only could use generator to create x coords based on y length
                    # print(len(x_coords))
                    # y_coords.append(meter_msg['Actual Value'])
                    y_coords.append(meter_msg['Display Value']) # append the read value to the coordinate data list
                    if (len(x_coords) > 0):
                        x_coords.append(x_coords[-1] + 1) # add the next value to the x_coords, note that this should probably be elapsed time
                    else:
                        x_coords.append(0)
                    if (len(y_coords) > graph_width): # if the dataset length is greater than the maximum size, remove the first value. this provides a FIFO buffer of values
                        del y_coords[0]
                        del x_coords[0]
                    
                    # print(f'{len(y_coords)},    {x_coords[-1]}, {y_coords[-1]}')
                    graph.set_ylabel(meter_msg['Display Unit'])
                    graph.update_graph(x_coords, y_coords)

                out_text = tenma.get_log_line_from_tenma_message(meter_msg)
                textbox.insert('end',out_text + '\n')

            # print(out_text)

                try:
                    log_data(log_file, meter_msg)
                except:
                    print(f"EXCEPTION! flogging -> {log_file} - meter_msg:{meter_msg}")

            except:
                print(f"EXCEPTION! data read -> {data}")
                print(traceback.format_exc())
                pass # if we have a dodgy message, just skip it
                lbl_serial_rx['text'] = data

            # print(out_text)

    # last_b_logging = b_logging            
    window.after(10,main_program_loop) # run this every 10 milli seconds

########## GRAPH FUNCTIONS ##########

def set_cbo_ports_values():
    list_of_ports = get_list_of_available_com_ports() #('/dev/ttyUSB0','/dev/ttyUSB1','COM17')
    if len(list_of_ports) == 0:
        list_of_ports = ['NO SERIAL PORTS']
    cbo_ports['value'] = list_of_ports
    cbo_ports.current(0) # start the box on the first value in the list

def reset_graph():
    global x_coords
    global y_coords
    global graph_width
    x_coords = []
    y_coords = []
    graph_width = int(cbo_graph_width.get())
    # print(f'Graph Width: {graph_width}')
    graph.reset_graph()
    # print('reset graph')

def save_graph():
    graph_filename = get_path_to_save_file(default_filename = create_default_filename('','png'))
    print(f"Saving logfile as {graph_filename}...")
    graph.save_graph(graph_filename)

""" DEFINE GUI WIDGETS """

tenma = tenma_interpreter.TenmaMeterSerialMsgs()

window = tk.Tk()
window.title('Tenma 72-2610 Multimeter Interface')

cbo_ports = ttk.Combobox(window)
# this list comprehension takes the port objects in the list returned by the comports method
# and returns a list of their device names
# otherwise it populates the combo box with the description string which can't be used to 
# open the port
# list_of_ports = get_list_of_available_com_ports() #('/dev/ttyUSB0','/dev/ttyUSB1','COM17')
# if list_of_ports == 0:
#     list_of_ports = ['NO SERIAL PORTS']
# cbo_ports['value'] = list_of_ports
# cbo_ports.current(0) # start the box on the first value in the list
set_cbo_ports_values()

#create the canvas
graph = tkgraph.tkGraph(window)
#graph2 = tkgraph.tkGraph(window)

cbo_speed = ttk.Combobox(window)
cbo_speed['values'] = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)
cbo_speed.current(2)
btn_com_port_refresh = tk.Button(window, text='Refresh', command=set_cbo_ports_values)

lbl_graph_width = tk.Label(window, text='Graph time [s]', justify='left')
cbo_graph_width = ttk.Combobox(window)
cbo_graph_width['values'] = (60,180,300,600,3600)
cbo_graph_width.current(0)

btn_open = tk.Button(window, text='CONNECT',command=open_close_port)

textbox = tk.scrolledtext.ScrolledText(window, width=50, height=4)
btn_graph_on = tk.Button(window, text='START GRAPH')#, command=toggle_graphing)

tx_text = tk.Entry(window, width=30)
tx_text.focus()
btn_transmit = tk.Button(window, text='TRANSMIT', command=send_serial)
led_rec = tkLED.LED(window, on_colour='#FFFFCC', off_colour='white')
btn_log = tk.Button(window, text='Start Log', command=toggle_log,  padx=30)
btn_reset = tk.Button(window, text='Reset Graph', command=reset_graph)
btn_save_graph = tk.Button(window, text='Save Graph', command=save_graph)

lbl_serial_rx = tk.Label(window, text='serial comes out here')

lbl_display_val = tk.Label(window, text='------', justify='center', font=('Arial',50), anchor=tk.CENTER, pady=2)

# cbo_log_period = ttk.Combobox(window)
# cbo_log_period['values'] = ['natural', '30 secs', '1 minute', '5 mins', '10 mins']
# cbo_log_period.current(0)

led_log = tkLED.LED(window, on_colour='#FFFFCC', off_colour='white')

""" DEFINE GUI LAYOUT """
# row 0
cbo_ports.grid( row=0,  column=0, sticky=tk.EW)
btn_com_port_refresh.grid(row=0,  column=1, sticky=tk.W)
# cbo_speed.grid( row=0,  column=1) # removed as it is not used
btn_open.grid(  row=0,  column=2, sticky=tk.NSEW)

# row 1
led_rec.grid(       row=1,  column=0, sticky=tk.NW)
lbl_display_val.grid(row=1, column=0, sticky=tk.NSEW, columnspan=3)
led_rec.lift(lbl_display_val) # lift() and lower() can be used to overlay widgets in the same place on the grid
# this is lifting the lbl_rec above the lbl_display_val


# row 2 
graph.grid(row=2,  column=0, columnspan=3,sticky=tk.NSEW) # , side=tk.TOP, fill=tk.BOTH, expand=1) # Graph display

# row 3
# cbo_log_period.grid( row=3, column=0, sticky=tk.W)
btn_reset.grid(       row=3,  column=0, sticky=tk.NSEW)
btn_save_graph.grid(       row=3,  column=1, sticky=tk.NSEW)
led_log.grid(       row=3,  column=2, sticky=tk.W)
btn_log.grid(       row=3,  column=2) #sticky=tk.CENTER, padx=10)

#tx_text.grid(       row=3,  column=0,   columnspan=2)
#btn_transmit.grid(  row=3,  column=2)

# row 4
btn_graph_on.grid(  row=4,  column=0, sticky=tk.NSEW)
lbl_graph_width.grid(  row=4,  column=1, sticky=tk.E)
cbo_graph_width.grid(  row=4,  column=2)

#graph2.grid(row=5,  column=0, columnspan=3,sticky=tk.NSEW) # , side=tk.TOP, fill=tk.BOTH, expand=1) # Graph display

# row 5
# lbl_serial_rx.grid(         row=5, column=0,  sticky='e')

# row 6
# textbox.grid(   row=6,  column=0,   columnspan=3)

### INITIALISATIONS ###

b_clear_list = False

messages_rec = []
msg_rec = bytearray()
rec_length = 0
num_reads = 30

list_length = 30

graph_width = int(cbo_graph_width.get())
print(f'Graph Width: {graph_width}')

# x_coords = [i for i in range(60)]
# y_coords = [0 for i in range(60)]

x_coords = []
y_coords = []

b_rec = False
b_reading = True
read_count = 0
tenma_header = tenma.get_tenma_722610_msg_header() #f"Time,Mode,Display Value,Display Unit,Actual Value,Actual Unit,AD/DC,Reading Type,Hold,Meter State,Bar Graph State,Bar Graph Value,Z1,Z2,Z2,Z4"
b_ser_port_open = False
b_graph_active = False
b_logging = False
last_b_logging = False
log_file = None
meter_msg = {}
ser = serial.Serial()

main_program_loop()
window.mainloop()
