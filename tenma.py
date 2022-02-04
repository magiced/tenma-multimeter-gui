# library for decoding tenman multimeter messages
import datetime

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
def get_mode(SB3,SB4):
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
    
def get_scale_multiplier(SB2, SB3):
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

def get_scale_prefix(SB2, SB3):
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
    
def get_unit(SB3, SB4):
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
    
def get_AC_DC(SB1):
    if SB1[4] == True:
        return "DC"
    elif SB1[3] == True:
        return "AC"
    else:
        return "-"
    
def get_reading_type(SB1,SB2):
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
    
def get_hold_status(SB1):
    if SB1[1] == True:
        return 'HOLD'
    else:
        return '-'
    
def get_meter_state(SB2):
    if SB2[2] == True:
        return 'Low Batt'
    elif SB2[3] == True:
        return 'Auto Power Off'
    else:
        return "-"

def get_bar_graph_state(SB1):
    if SB1[0] == True:
        return 'On'
    else:
        return 'Off'

def get_user_symbol_Z1(SB2):
    if SB2[7] == True:
        return 'Z1 On'
    else:
        return 'Z1 Off'

def get_user_symbol_Z2(SB2):
    if SB2[6] == True:
        return 'Z2 On'
    else:
        return 'Z2 Off'

def get_user_symbol_Z3(SB2):
    if SB2[0] == True:
        return 'Z3 On'
    else:
        return 'Z3 Off'

def get_user_symbol_Z4(SB3):
    if SB3[0] == True:
        return 'Z4 On'
    else:
        return 'Z4 Off'

def get_tenma_vals_from_ser_msg(msg_in):
    point = msg_in[6] & 0b00001111
    mystery_nibble = (msg_in[6] >> 4) & 0b0000111 # i don't know what this is or does!

    if (msg_in[1:5] == b'?0:?'):
        value = 'OL'
        b_OL = True
    else:
        value = int( msg_in[:5].decode() ) / get_decimal_point_divider(point)
        b_OL = False

    SB1 = get_bitfield_from_byte(msg_in[7],False)
    SB2 = get_bitfield_from_byte(msg_in[8],False)
    SB3 = get_bitfield_from_byte(msg_in[9],False)
    SB4 = get_bitfield_from_byte(msg_in[10],False)

    bar = get_bar_graph_value(msg_in[11])
    # don't care about these values
    space = msg_in[5]
    eof = msg_in[12]
    enter = msg_in[13]

    time_now = datetime.datetime.now().isoformat()
    mode = get_mode(SB3,SB4)
    disp_value = value
    display_unit = get_scale_prefix(SB2, SB3) + get_unit(SB3, SB4)
    if value == 'OL':
        actual_value = value
    else:    
        actual_value = value * get_scale_multiplier(SB2, SB3)
    actual_unit = get_unit(SB3, SB4)
    ac_dc = get_AC_DC(SB1)
    reading_type = get_reading_type(SB1,SB2)
    hold = get_hold_status(SB1)
    meter_state = get_meter_state(SB2)
    bar_graph_state = get_bar_graph_state(SB1)
    bar_graph_value = bar
    Z1_state = get_user_symbol_Z1(SB2)
    Z2_state = get_user_symbol_Z2(SB2)
    Z3_state = get_user_symbol_Z3(SB2)
    Z4_state = get_user_symbol_Z4(SB3)

    #TODO - create dict to return of data from this f"{time_now},{mode},{disp_value},{display_unit},{actual_value},{actual_unit},{ac_dc},{reading_type},{hold},{meter_state},{bar_graph_state},{bar_graph_value},{Z1_state},{Z2_state},{Z3_state},{Z4_state}"

    dict_out = {'Time':time_now,
                'Mode':mode,
                'OL': b_OL,
                'Display Value':disp_value,
                'Display Unit':display_unit,
                'Actual Value':actual_value,
                'Actual Unit':actual_unit,
                'AD/DC':ac_dc,
                'Reading Type':reading_type,
                'Hold':hold,
                'Meter State':meter_state,
                'Bar Graph State':bar_graph_state,
                'Bar Graph Value':bar_graph_value,
                'Z1':Z1_state,
                'Z2':Z2_state,
                'Z3':Z3_state,
                'Z4':Z4_state,
                }

    return dict_out