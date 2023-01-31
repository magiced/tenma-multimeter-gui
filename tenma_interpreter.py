import datetime

class TenmaMeterSerialMsgs():

    """
    This class interprets the serial messages from 
    the tenma multimeter into useful readable data
    """
    def __init__(self):
        pass

    def get_decimal_point_divider(self, nibble_in):
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


    def get_bitfield_from_byte(self, byte_in, b_reverse=True):
        """ produces a list of bits. the list can be reversed to make the bit order look correct
            or left in the original order to match the bit mumbering with the list index """
        bitfield = []
        for i in range(8):
            x = (byte_in >> i) & 0x01
            bitfield.append(x)
        if b_reverse:
            bitfield.reverse() # reverse so that the bits are the right way round
        return bitfield

    def get_bar_graph_value(self, byte_in):
        """ returns the value of the bar graph byte with the correct sign"""
        b_sign = (byte_in >> 7) & 0x01
        number = int(byte_in & 0b01111111)
        
        if b_sign:
            return number
        else:
            return number * -1
        
    # note, in order to make the lookup match the datasheet,
    # they bytes have not been reversed when getting the bitfield
    def get_mode(self):

        if self.SB3[2] == True:
            return "Diode Test"
        elif self.SB4[7] == True:
            return "Voltage"
        elif self.SB4[6] == True:
            return "Current"
        elif self.SB4[5] == True:
            return "Resistance"
        elif self.SB3[3] == True:
            return "Continuity"
        elif self.SB4[3] == True:
            return "Frequency"
        elif self.SB4[2] == True:
            return "Capacitance"
        elif (self.SB4[1] == True) or (self.SB4[0] == True):
            return "Temperature"
        elif self.SB3[1] == True: # Percent
            return "Duty Cycle"
        else:
            return "Unknown"
        
    def get_scale_multiplier(self):
        if self.SB2[1] == True: # nano
            return 0.000000001
        elif self.SB3[7] == True: #micro
            return 0.000001
        elif self.SB3[6] == True: #milli
            return 0.001
        elif self.SB3[5] == True: # kilo
            return 1000
        elif self.SB3[4] == True: # mega
            return 1000000
        else:
            return 1 # no scaling value

    def get_scale_prefix(self):
        if self.SB2[1] == True: # nano
            return "n"
        elif self.SB3[7] == True: #micro
            return "µ"
        elif self.SB3[6] == True: #milli
            return "m"
        elif self.SB3[5] == True: # kilo
            return "k"
        elif self.SB3[4] == True: # mega
            return "M"
        else:
            return "" # no scaling value    
        
    def get_unit(self):
        if self.SB4[7] == True: # "Voltage"
            return "V"
        elif self.SB4[6] == True: # "Current"
            return "A"
        elif self.SB4[5] == True: # "Resistance"
            return "Ω"
        elif self.SB3[3] == True: # "Continuity"
            return "Ω"
        elif self.SB3[2] == True: # "Diode Test" - not sure about this
            return "hFE?"
        elif self.SB4[3] == True: # "Frequency"
            return "Hz"
        elif self.SB4[2] == True: # "Capacitance"
            return "F"
        elif self.SB4[1] == True: # "Temperature - Celsius"
            return "°C"
        elif self.SB4[0] == True: # "Temperature - Fahrenheit"
            return "°F"
        elif self.SB3[1] == True: # Percent
            return "%"
        else:
            return "Unknown"
        
    def get_AC_DC(self):
        if self.SB1[4] == True:
            return "DC"
        elif self.SB1[3] == True:
            return "AC"
        else:
            return "-"
        
    def get_reading_type(self):
        if self.SB1[5] == True:
            return 'Auto'
        elif self.SB1[2] == True:
            return "Rel"
        elif self.SB2[5] == True:
            return 'Max'
        elif self.SB2[4] == True:
            return 'Min'
        else:
            return "-"
        
    def get_hold_status(self):
        if self.SB1[1] == True:
            return 'HOLD'
        else:
            return '-'
        
    def get_meter_state(self):
        if self.SB2[2] == True:
            return 'Low Batt'
        elif self.SB2[3] == True:
            return 'Auto Power Off'
        else:
            return "-"

    def get_bar_graph_state(self):
        if self.SB1[0] == True:
            return 'On'
        else:
            return 'Off'

    def get_user_symbol_Z1(self):
        if self.SB2[7] == True:
            return 'Z1 On'
        else:
            return 'Z1 Off'

    def get_user_symbol_Z2(self):
        if self.SB2[6] == True:
            return 'Z2 On'
        else:
            return 'Z2 Off'

    def get_user_symbol_Z3(self):
        if self.SB2[0] == True:
            return 'Z3 On'
        else:
            return 'Z3 Off'

    def get_user_symbol_Z4(self):
        if self.SB3[0] == True:
            return 'Z4 On'
        else:
            return 'Z4 Off'

    def get_tenma_722610_msg_header(self):
        output_file_header = f"Time,Timestamp,Mode,OL,Display Value,Display Unit,Actual Value,Actual Unit,AD/DC,Reading Type,Hold,Meter State,Bar Graph State,Bar Graph Value,Z1,Z2,Z3,Z4"
        return output_file_header

    def interpret_tenma_722610_msg(self, msg_rec):
    # this needs to go into the multimeter class
        point = msg_rec[6] & 0b00001111
        mystery_nibble = (msg_rec[6] >> 4) & 0b0000111 # i don't know what this is or does!

        if (msg_rec[1:5] == b'?0:?'):
            value = 'OL'
            b_OL = True
        else:
            value = int( msg_rec[:5].decode() ) / self.get_decimal_point_divider(point)
            b_OL = False

        self.SB1 = self.get_bitfield_from_byte(msg_rec[7],False)
        self.SB2 = self.get_bitfield_from_byte(msg_rec[8],False)
        self.SB3 = self.get_bitfield_from_byte(msg_rec[9],False)
        self.SB4 = self.get_bitfield_from_byte(msg_rec[10],False)

        bar = self.get_bar_graph_value(msg_rec[11])
        # don't care about these values
        space = msg_rec[5]
        eof = msg_rec[12]
        enter = msg_rec[13]

        time_now = datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().timestamp()
        mode = self.get_mode()
        disp_value = value
        display_unit = self.get_scale_prefix() + self.get_unit()
        if value == 'OL':
            actual_value = value
        else:    
            actual_value = value * self.get_scale_multiplier()
        actual_unit = self.get_unit()
        ac_dc = self.get_AC_DC()
        reading_type = self.get_reading_type()
        hold = self.get_hold_status()
        meter_state = self.get_meter_state()
        bar_graph_state = self.get_bar_graph_state()
        bar_graph_value = bar
        Z1_state = self.get_user_symbol_Z1()
        Z2_state = self.get_user_symbol_Z2()
        Z3_state = self.get_user_symbol_Z3()
        Z4_state = self.get_user_symbol_Z4()

        dict_out = {'Time':time_now,
            'Timestamp':timestamp,
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

    def get_log_line_from_tenma_message(self, msg_in):
        log_line = f"{msg_in['Time']},{msg_in['Timestamp']},{msg_in['Mode']},{msg_in['OL']},{msg_in['Display Value']},{msg_in['Display Unit']},{msg_in['Actual Value']},{msg_in['Actual Unit']},{msg_in['AD/DC']},{msg_in['Reading Type']},{msg_in['Hold']},{msg_in['Meter State']},{msg_in['Bar Graph State']},{msg_in['Bar Graph Value']},{msg_in['Z1']},{msg_in['Z2']},{msg_in['Z3']},{msg_in['Z4']}"
        return log_line

        # # reading output line
        # output_string = f"{time_now},{mode},{disp_value},{display_unit},{actual_value},{actual_unit},{ac_dc},{reading_type},{hold},{meter_state},{bar_graph_state},{bar_graph_value},{Z1_state},{Z2_state},{Z3_state},{Z4_state}"
        # return output_string
        