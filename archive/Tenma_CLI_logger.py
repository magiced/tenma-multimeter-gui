import time
import serial
import serial.tools.list_ports

from easyfiledialogs import get_path_to_save_file
import tenma_interpreter

##############
# VIEW CLASS #
##############

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

def get_datetime_string():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

#TODO - this does not replace every slash in a text string such as \dev\tty4, it onle produces -dev\tty4
def create_default_filename():
    return f"{get_datetime_string()} Tenma Multimeter Log.csv"
 

# ser.close()
# ser.close()
# ser.port(cbo_ports.get())
# ser.baudrate(cbo_speed.get())
# ser.open()

#########
# MODEL #
#########
"""
This class provides the interpretation of the serial messages from 
the multimeter into readable data
It does not read the data, or display it
"""

    

#####################
# Serial Port Class #
#####################

def get_available_com_ports():
    print("Finding ports...")
    ports = serial.tools.list_ports.comports()
#     print("Available ports:")
#     for i in ports:
#         print(" - " + i.name)
    return ports







#################
# Logging Class #
#################



##################
### Controller ###
##################
"""
This class is the main part of the program.
it calls the view class to get input from the user - serial port and log filename
it uses the view, multimeter interpreter and the serial port class
it opens the serial port
it uses the serial message interpreter on the data recieved
it then displays that data on the CLI
it logs the data using the logging class

the idea of this is for me to classify the serial port and the multimeter 

    
# # write line
# for i in range(10):
#     with open('testlog.csv', 'a') as x:
#         x.write(f'{i},bees\n')

# check what serial ports available
# print to ask user which port to open
# wait for user input
# select serial port the user selects
# generate default log file name
# ask user where to log file to
# display log filename
# open file
# save log header
# open serial port user has asked
# recieve data  message from port
# translate data message
# display data message
# log data message
# monitor for keyboard interrupt
# if keyboard interrupt recieved close serial port and log file
# exit program
"""

messages_rec = []
msg_rec = bytearray()
rec_length = 0
num_reads = 30

b_reading = True
read_count = 0

print()

tenma = tenma_interpreter.TenmaMeterSerialMsgs()

serial_speeds = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)

available_ports = get_available_com_ports() # finds the com ports on the system

if len(available_ports) == 0:
    print("There are no com ports available, program closing")
    quit()

serial_speeds = (300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400)

port_to_open = get_item_from_menu(available_ports, "Select a Serial Port").name # creates a menu to select the serial port from

serial_speed = 2400


                                                 
print(f"\nOpening Serial port {port_to_open} at {serial_speed} baud...\n")

# try:
#     ser.close() # close the serial port if it's open
# except NameError:
#     pass

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
print('Serial Port Open')
ser.setRTS(False) # required for tenma meters, as these lines power the optical reciever circuit
ser.setDTR(True) 
ser.readline() # make sure we can read (may be incomplete)


log_filename = get_path_to_save_file(default_filename = create_default_filename())
print(f"Saving logfile as {log_filename}...")
logfile = open(log_filename, 'w', encoding="utf-8")

# this is the log file start function
output_file_header = tenma.get_tenma_722610_msg_header()
print(output_file_header)

# write header
with open(log_filename, 'w') as logfile:
    logfile.write(output_file_header + '\n')

# this is the main loop
# add keyboard interrupt check to stop logging
print()
print('Logging started, press CTRL + C to stop logging')
print()

while (b_reading):
    try:
        # recieve serial data
        msg_rec = ser.readline()
        # print(len(msg_rec))
        output_string = tenma.interpret_tenma_722610_msg(msg_rec)
        # put data into interpreter to translate message
        
        # View - print data line
        print(output_string)

        # log line
        with open(log_filename, 'w') as logfile:
            logfile.write(output_string + '\n')

    #    read_count += 1
    #    if read_count > num_reads:
    #        b_reading = False
    #        print(f"{read_count} number of line read, closing...\n")
        
    except KeyboardInterrupt:
        print('Keyboard Interrupt Detected, stopping log')
        break

# needs a way to stop the log (although am not that bothered about this as this is just a lead up to the gui)
print("Closing log file...")
logfile.close()    

print("Closing port...")
ser.close()    

print('Finished!')


    