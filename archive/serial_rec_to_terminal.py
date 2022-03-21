import time
import datetime
import serial
import serial.tools.list_ports

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shelve

def get_datetime_string():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def get_filename_with_tkinter():
    shelfFile = shelve.open('mydata')

    # try to open saved variables from shelfFile, if the saved variables are not there,
    # set the last open variable to "/"
    try:
        last_open_dir = shelfFile['last_open_dir']
    except KeyError:
        last_open_dir = "/"

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    this_file =  Path(filedialog.askopenfilename(initialdir = last_open_dir,title = "Select file",filetypes = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))))
    root.destroy()

    # save the last opened folder to the shelfFile
    shelfFile['last_open_dir'] = this_file.parent
    shelfFile.close()
    
    return this_file

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

def get_available_com_ports():
    print("Finding ports...")
    ports = serial.tools.list_ports.comports()
#     print("Available ports:")
#     for i in ports:
#         print(" - " + i.name)
    return ports

def print_menu(items):
    for i in range(len(items)):
        print(f"{i+1}: {items[i]}")
        
def get_item_from_menu(items, title="Select an item:", default=""):
    # default is the line of the default item
    print("")
    print(title)
    print_menu(items)

    num_items = len(items)
    print(f"Pick an item between 1 and {num_items}")
    
    b_correct_input = False
    if num_items == 1:
        print(f"Only '{items[0]}' available")
        response = 1
        b_correct_input = True
        
    if default != "":
        print(f"Press enter for default value: {default}")
        
    while (not b_correct_input):
        response = input("Select >>")
#         print(bytes(response))
        if (response == "") & (default != ""):
            response = default
            print("Default selected")
            break
        if not response.isdecimal():
            print("Please input a number")
            continue
        if int(response) > num_items:
            print("Number too high")
            continue
        if int(response) < 1:
            print("Number too low")
            continue
        b_correct_input = True
    
    selected_line = int(response)
    item_out = items[selected_line - 1]
    print(f"{item_out} selected")
    return item_out     

# ser.close()
# ser.close()
# ser.port(cbo_ports.get())
# ser.baudrate(cbo_speed.get())
# ser.open()

#TODO - this does not replace every slash in a text string such as \dev\tty4, it onle produces -dev\tty4
def create_default_filename():
    return f"{get_datetime_string()} Tenma Multimeter Log.csv"

### ========== Multimeter Functions ========== ###


def get_decimal_point_divider(nibble_in):
    if (nibble_in == 0x00):
        return 1
    elif (nibble_in == 0x01):
        return 1000
    elif( nibble_in == 0x02):
        return 100
    elif (nibble_in == 0x04):
        return 10
    else:
        return 1

# produces a list of bits. the list can be reversed to make the bit order look correct
# or left in the original order to match the bit mumbering with the list index
def get_bitfield_from_byte(byte_in, b_reverse=True):
    bitfield = []
    for i in range(8):
        x = (byte_in >> i) & 0x01
        bitfield.append(x)
    if b_reverse:
        bitfield.reverse() # reverse so that the bits are the right way round
    return bitfield

def get_bar_graph_value(byte_in):
    b_sign = (byte_in >> 7) & 0x01
    number = int(byte_in & 0b01111111)
    
    if b_sign:
        return number
    else:
        return number * -1
    
# note, in order to make the lookup match the datasheet,
# they bytes have not been reversed when getting the bitfield
def get_mode():
    if SB3[2] == True:
        return "Diode Test"
    elif SB4[7] == True:
        return "Voltage"
    elif SB4[6] == True:
        return "Current"
    elif SB4[5] == True:
        return "Resistance"
    elif SB3[3] == True:
        return "Continuity"
    elif SB4[3] == True:
        return "Frequency"
    elif SB4[2] == True:
        return "Capacitance"
    elif (SB4[1] == True) or (SB4[0] == True):
        return "Temperature"
    elif SB3[1] == True: # Percent
        return "Duty Cycle"
    else:
        return "Unknown"
    
def get_scale_multiplier():
    if SB2[1] == True: # nano
        return 0.000000001
    elif SB3[7] == True: #micro
        return 0.000001
    elif SB3[6] == True: #milli
        return 0.001
    elif SB3[5] == True: # kilo
        return 1000
    elif SB3[4] == True: # mega
        return 1000000
    else:
        return 1 # no scaling value

def get_scale_prefix():
    if SB2[1] == True: # nano
        return "n"
    elif SB3[7] == True: #micro
        return "µ"
    elif SB3[6] == True: #milli
        return "m"
    elif SB3[5] == True: # kilo
        return "k"
    elif SB3[4] == True: # mega
        return "M"
    else:
        return "" # no scaling value    
    
def get_unit():
    if SB4[7] == True: # "Voltage"
        return "V"
    elif SB4[6] == True: # "Current"
        return "A"
    elif SB4[5] == True: # "Resistance"
        return "Ω"
    elif SB3[3] == True: # "Continuity"
        return "Ω"
    elif SB3[2] == True: # "Diode Test" - not sure about this
        return "hFE?"
    elif SB4[3] == True: # "Frequency"
        return "Hz"
    elif SB4[2] == True: # "Capacitance"
        return "F"
    elif SB4[1] == True: # "Temperature - Celsius"
        return "°C"
    elif SB4[0] == True: # "Temperature - Fahrenheit"
        return "°F"
    elif SB3[1] == True: # Percent
        return "%"
    else:
        return "Unknown"
    
def get_AC_DC():
    if SB1[4] == True:
        return "DC"
    elif SB1[3] == True:
        return "AC"
    else:
        return "-"
    
def get_reading_type():
    if SB1[5] == True:
        return 'Auto'
    elif SB1[2] == True:
        return "Rel"
    elif SB2[5] == True:
        return 'Max'
    elif SB2[4] == True:
        return 'Min'
    else:
        return "-"
    
def get_hold_status():
    if SB1[1] == True:
        return 'HOLD'
    else:
        return '-'
    
def get_meter_state():
    if SB2[2] == True:
        return 'Low Batt'
    elif SB2[3] == True:
        return 'Auto Power Off'
    else:
        return "-"

def get_bar_graph_state():
    if SB1[0] == True:
        return 'On'
    else:
        return 'Off'

def get_user_symbol_Z1():
    if SB2[7] == True:
        return 'Z1 On'
    else:
        return 'Z1 Off'

def get_user_symbol_Z2():
    if SB2[6] == True:
        return 'Z2 On'
    else:
        return 'Z2 Off'

def get_user_symbol_Z3():
    if SB2[0] == True:
        return 'Z3 On'
    else:
        return 'Z3 Off'

def get_user_symbol_Z4():
    if SB3[0] == True:
        return 'Z4 On'
    else:
        return 'Z4 Off'

### ========== PROGRAM ========== ###

try:
    ser.close() # close the serial port if it's open
except NameError:
    pass
    
serial_speeds = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)

available_ports = get_available_com_ports() # finds the com ports on the system

if len(available_ports) == 0:
    print("There are no com ports available, program closing")
    quit()

serial_speeds = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)

port_to_open = get_item_from_menu(available_ports, "Select a Serial Port").name # creates a menu to select the serial port from

serial_speed = 2400

log_filename = get_file_save_name_with_tkinter(create_default_filename())
print(f"Saving logfile as {log_filename}...")
logfile = open(log_filename, 'w', encoding="utf-8")
  
                                               
print(f"\nOpening Serial port {port_to_open} at {serial_speed} baud...\n")

ser = serial.Serial()
ser.port = port_to_open
ser.baudrate = serial_speed
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 3
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 3
# ser.open()

"""open the serial port device"""
if ser.is_open:
    print("serial port already open")
    print("Attempting to close")
    ser.close()
    
ser.open()
ser.setRTS(False) # required for tenma meters, as these lines power the optical reciever circuit
ser.setDTR(True) 
ser.readline() # make sure we can read (may be incomplete)

messages_rec = []
msg_rec = bytearray()
rec_length = 0
num_reads = 30

b_reading = True
read_count = 0

print()

# logfile.write(output_file_header + '\n')

while (b_reading):
    print(ser.readline())
    # msg_rec = ser.readline()
    # # print(len(msg_rec))
    # point = msg_rec[6] & 0b00001111


#    read_count += 1
#    if read_count > num_reads:
#        b_reading = False
#        print(f"{read_count} number of line read, closing...\n") 

print("Closing port...")
ser.close()    

print('Finished!')


    