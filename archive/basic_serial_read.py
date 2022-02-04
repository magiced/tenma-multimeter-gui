import serial
import serial.tools.list_ports
import datetime


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



print("\n### TENMA MULTIMETER INTERFACE ###")
port="COM2"

print("Preparing to use",port)
ser = serial.Serial()
ser.port = port
ser.baudrate = 2400
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 3
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 3

"""open the serial port device"""
if ser.is_open:
    print("serial port already open")
    
print("connecting to",port,"...")
ser.open()
ser.setRTS(False) # required for tenma meters!
ser.setDTR(True) 
ser.readline() # make sure we can read (may be incomplete)

messages_rec = []
msg_rec = bytearray()
rec_length = 0

b_reading = True
read_count = 0

output_file_header = f"Time, Mode, Display Value, Display Unit, Actual Value, Actual Unit, AD//DC, Reading Type, Hold, Meter State, Bar Graph State, Bar Graph Value, Z1, Z2, Z2, Z4"
print(output_file_header)

while (b_reading):
    msg_rec = ser.readline()
    # print(len(msg_rec))
    point = msg_rec[6] & 0b00001111
    mystery_nibble = (msg_rec[6] >> 4) & 0b0000111 # i don't know what this is or does!

    if (msg_rec[1:5] == b'?0:?'):
        value = 'OL'
    else:
        value = int( msg_rec[:5].decode() ) / get_decimal_point_divider(point)

    SB1 = get_bitfield_from_byte(msg_rec[7],False)
    SB2 = get_bitfield_from_byte(msg_rec[8],False)
    SB3 = get_bitfield_from_byte(msg_rec[9],False)
    SB4 = get_bitfield_from_byte(msg_rec[10],False)

    bar = get_bar_graph_value(msg_rec[11])
    # don't care about these values
    space = msg_rec[5]
    eof = msg_rec[12]
    enter = msg_rec[13]

    time_now = datetime.datetime.now().isoformat()
    mode = get_mode()
    disp_value = value
    display_unit = get_scale_prefix() + get_unit()
    if value == 'OL':
        actual_value = value
    else:    
        actual_value = value * get_scale_multiplier()
    actual_unit = get_unit()
    ac_dc = get_AC_DC()
    reading_type = get_reading_type()
    hold = get_hold_status()
    meter_state = get_meter_state()
    bar_graph_state = get_bar_graph_state()
    bar_graph_value = bar
    Z1_state = get_user_symbol_Z1()
    Z2_state = get_user_symbol_Z2()
    Z3_state = get_user_symbol_Z3()
    Z4_state = get_user_symbol_Z4()

    # reading output line
    output_string = f"{time_now},{mode},{disp_value},{display_unit},{actual_value},{actual_unit},{ac_dc},{reading_type},{hold},{meter_state},{bar_graph_state},{bar_graph_value},{Z1_state},{Z2_state},{Z3_state},{Z4_state}"
    print(output_string)
