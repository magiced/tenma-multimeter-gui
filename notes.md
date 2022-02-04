https://github.com/swharden/pyTENMA


http://www.wattnotions.com/tenma-72-7735-serial-interface/


https://stackoverflow.com/questions/17700370/reading-data-from-a-tenma-72-7732-multimeter-using-pyusb

"I use a simple IR to RS232 adapter which consists of an IR detector strapped Anode to pin 4 and cathode to pin 2 (RX data). When hooked up to my PC with a simple terminal set to 2400 Baud, 7 Data 1 Stop, No parity, No handshake it produces the following string

013651211

which repeats about every 400 ms. The first 5 digits are as read on the meter, digit 6 is decimal point location, digit 8 is function position

VDC = 1 AmpDC = 9

Last digit seems to be auto/manual mixed with sign; the rest I don't need (yet)."


https://swharden.com/blog/2016-08-24-tenma-multimeter-serial-hack/

https://www.element14.com/community/docs/DOC-42352/l/software-for-tenma-72-7735-for-windows7-rs232-protocol-information-flie

try adjusting dts and rts pins to get teraterm output

finding OEM of multimeter

looks like a UNI-TREND UT61
https://www.uni-trend.com/meters/html/product/General_Meters/DigitalMultimeters/UT61_Series/

this describes the serial protocol and what to set to get working
http://www.starlino.com/uni-t-ut61e-multimiter-serial-protocol-reverse-engineering.html

http://gushh.net/blog/ut61e-protocol/

using program "termite" for the serial connection, as it has better control of RTS and DTS lines, using the LED plugin
https://www.compuphase.com/software_termite.htm

using "Free device monitoring studio"

buad rate: 2400
clear RTS
set DTR
set line control
    word length = 8
    stop bits = 1 stop bit
    parity = No Parity
Set special chars
    EofChar=0x0
  ErrorChar=0x0
  BreakChar=0x0
  EventChar=0x0
  XonChar=0x11
  XoffChar=0x13
Set handshake information
  ControlHandShake=1
  FlowReplace=0
  XonLimit=512
  XoffLimit=1

SUCCESS!

got it working with the following settings:
Baud 2400
Byte Size: 8
Parity: None
Stop Bit: 1
RTS: LOW
DTR: HIGH

pyTENMA script doesn't decode the bytes without esception
+2802 41[00]@€[1B]
+2801 41[00]@€[1C]
+2801 41[00]@€[1C]
+2801 41[00]@€[1B]
+2801 41[00]@€[1B]
+2801 41[00]@€[1C]
+2802 41[00]@€[1C]
+2802 41[00]@€[1B]
+2802 41[00]@€[1C]
+2803 41[00]@€[1B]
+2803 41[00]@€[1C]

2b 32 38 30 30 20 34 31 00 40 80 1c 0d 0a        +2800 41.@€...  
2b 32 38 30 30 20 34 31 00 40 80 1c 0d 0a        +2800 41.@€...  
2b 32 37 39 39 20 34 31 00 40 80 1c 0d 0a        +2799 41.@€...  
2b 32 37 39 39 20 34 31 00 40 80 1c 0d 0a        +2799 41.@€...  
2b 32 37 39 39 20 34 31 00 40 80 1b 0d 0a        +2799 41.@€...  
2b 32 38 30 30 20 34 31 00 40 80 1c 0d 0a        +2800 41.@€...  
2b 32 38 30 30 20 34 31 00 40 80 1b 0d 0a        +2800 41.@€...

UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 10: ordinal not in range(128)

https://docs.python.org/3/library/codecs.html#standard-encodings

https://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte

## Required changes

- [] add speed and type to py tenma call
- [x] create new formatVal function

## different outputs

b'+3662 41\x00@\x80$\r\n' -> +3662 41@$ - Volts
b'+1641 21\x00@\x80\x10\r\n' -> +1641 21@► - milliVolts
b'+?0:? 1!\x00  =\r\n' -> +?0:? 1!  = - ohms
b'+?0:? 1!\x00\x10 =\r\n' -> +?0:? 1!► =
b'+?0:? 2!\x00\x10 =\r\n' -> +?0:? 2!► =
b'+?0:? 2!\x00\x10 =\r\n' -> +?0:? 2!► =
b'+?0:? 2!\x00\x10 =\r\n' -> +?0:? 2!► =
b'+?0:? 2!\x00\x10 =\r\n' -> +?0:? 2!► =
b'+0000 1 \x00\x00\x08=\r\n' -> +0000 1=
b'+5001 2 \x00\x00\x08=\r\n' -> +5001 2=
b'+5001 2 \x00\x00\x08=\r\n' -> +5001 2=
b'+4998 2 \x00\x00\x08=\r\n' -> +4998 2=
b'+5001 2 \x00\x00\x08=\r\n' -> +5001 2=
b'+4999 2 \x00\x00\x08=\r\n' -> +4999 2=
b'+4999 2 \x00\x00\x08=\r\n' -> +4999 2=
b'+4999 0\x00\x00\x00\x02=\r\n' -> +4999 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 0\x00\x00\x00\x02=\r\n' -> +?0:? 0☻=
b'+?0:? 01\x00\x00@\x00\r\n' -> +?0:? 01@
b'+0000 41\x00\x80@\x00\r\n' -> +0000 41@ - current microAmps
b'+0000 21\x00@@\x00\r\n' -> +0000 21@@ - current milliAmps
b'+0000 11\x00\x00@\x00\r\n' -> +0000 11@ - current Amps

Volts - 
  b'+0052 41\x00@\x80\x00\r\n'
  b'+0000 41\x00@\x80\x00\r\n'(when resistance there)
  b'+3574 11\x00\x00\x80#\r\n'(when on batt cell)
milliVolts
  b'-0055 21\x00@\x80\x80\r\n'
  b'+0000 21\x00@\x80\x00\r\n' (when resistance there)
Resistance
  b'+?0:? 2!\x00\x10 =\r\n' (OL)
  b'+1196 4!\x00  \x0b\r\n' (when resistance there)
Frequency
  b'+5006 2 \x00\x00\x08=\r\n'
Temperature
  b'-0113 0\x00\x00\x00\x02=\r\n' (when resistance there)
  b'+?0:? 0\x00\x00\x00\x02=\r\n' (OL)
microAmps
  b'+0000 41\x00\x80@\x00\r\n' (zero current)
milliAmps
  b'+0000 21\x00@@\x00\r\n' (zero current)
Amps
  b'+0000 11\x00\x00@\x00\r\n' (zero current)

## multimeter chip
Semic CS7729CN 001 QHAA1S3S3HY

protocol appears to be the same as in this doc: http://improwis.com/projects/reveng_multimeters/chips/FS9922-DMM3-DS-11_EN.pdf


## BYTES
so, i think the transmission protocol uses bits and bytes etc. Now i have to work out how to use these comforatbly in python

https://docs.python.org/3/library/stdtypes.html#bytes-methods

## Next Actions
- make status byte dictionary

status_SB1 = {
"reserved1" : False, #reserved
"reserved2" : False,
"auto" : False,
"DC" : False,
"AC" : False,
"REL" : False,
"HOLD" : False,
"BPN" : False,
}

status_SB2 = {
"Z1" : False, #reserved
"Z2" : False,
"MAX" : False,
"MIN" : False,
"APO" : False,
"Bat" : False,
"n" : False,
"Z3" : False,
}

status_SB3 = {
"scale_micro" : False, #reserved
"scale_milli" : False,
"scale_kilo" : False,
"scale_mega" : False,
"mode_continuity" : False,
"mode_diode_test" : False,
"scale_percent" : False,
"Z4" : False,
}

status_SB3 = {
"mode_voltage" : False, #reserved
"mode_current" : False,
"mode_resistance" : False,
"mode_capacitance" : False,
"mode_frequency" : False,
"mode_F" : False,
"scale_celsius" : False,
"scale_fahrenheit" : False,
}

## matplotlib and python

https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/all


## last error

EXCEPTION! flogging -> None - meter_msg:{'Time': '2021-10-06T17:57:58.125669', 'Mode': 'Voltage', 'Display Value': 4.097, 'Display 
Unit': 'V', 'Actual Value': 4.097, 'Actual Unit': 'V', 'AD/DC': 'DC', 'Reading Type': 'Auto', 'Hold': '-', 'Meter State': '-', 'Bar Graph State': 'On', 'Bar Graph Value': -40, 'Z1': 'Z1 Off', 'Z2': 'Z2 Off', 'Z3': 'Z3 Off', 'Z4': 'Z4 Off'}
Exception in Tkinter callback
Traceback (most recent call last):
  File "c:\Users\ed.bisdee\OneDrive - Hyperdrive Innovation 365\Documents\_code\tenma-multimeter-interface\tenma-dmm-gui.py", line 
476, in main_program_loop
    log_data(log_file, meter_msg)
  File "c:\Users\ed.bisdee\OneDrive - Hyperdrive Innovation 365\Documents\_code\tenma-multimeter-interface\tenma-dmm-gui.py", line 
330, in log_data
    log_data_line(log_file, data_line_string)
  File "c:\Users\ed.bisdee\OneDrive - Hyperdrive Innovation 365\Documents\_code\tenma-multimeter-interface\tenma-dmm-gui.py", line 
323, in log_data_line
TypeError: expected str, bytes or os.PathLike object, not NoneType

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\ed.bisdee\AppData\Local\Programs\Python\Python39\lib\tkinter\__init__.py", line 1884, in __call__
    return self.func(*args)
  File "C:\Users\ed.bisdee\AppData\Local\Programs\Python\Python39\lib\tkinter\__init__.py", line 805, in callit
    func(*args)
  File "c:\Users\ed.bisdee\OneDrive - Hyperdrive Innovation 365\Documents\_code\tenma-multimeter-interface\tenma-dmm-gui.py", line 
479, in main_program_loop
    raise exception
NameError: name 'exception' is not defined

## logging and debugging

considering using the logging library for the logging output
- update, nahhh, it's not the right thing

http://automatetheboringstuff.com/2e/chapter11/

https://realpython.com/python-logging/

https://docs.python.org/3/library/logging.html

## making a log file library

required functions
init function
write line - writes string to log as single line
set header - defualt: no header, otherwise writes header
stop logging - close file
start logging - start logging
create log file - create log file 

## gauge output
b'0.000000\r\n' # note, it's not actually bytes

    bytes_in = ser.read_until() #read the data from the serial port, strip the line feed from it, then convert from bytes to a string
    data_in = bytes_in.strip().decode() #read the data from the serial port, strip the line feed from it, then convert from bytes to a string
    time_in = datetime.datetime.now().isoformat()
    log_line = bytes_in
#     log_line = time_in + "," + str(data_in) + ',' + data_in
    print(log_line) #read until end of line
    with open(log_filename,'a') as f_out:
        f_out.write(log_line + '\n')

this works great, should probably send f message to start with to make sure it's transmitting at 1 sec, and maybe ignore speed lines

Speed:60s
-0.005000
Speed:1s
-0.005000
-0.005000
-0.005000

## Using TTL-232R-5V cable
This does not work immediately, as the RTS has to be low (False), and the DTR has
to be high to supply power to the recieving circuit in the meter cable.

The TTL cable does not have a DTR line, so this won't work. I think i will have to try connecting VCC (red) to D9 pin 4 and ground to D9 pin 7.

## db9 pinout
### multimeter interface cable
1 - NC
2 - RXD - Recieve Data - Brown
3 - TXD - Transmit Data - White
4 - DTR - Data Terminal Ready - Orange
5 - GND - Signal Ground - Yellow
6 - DSR - Data Set Ready - Looped to 4
7 - RTS - Request to Send - Green and looped to 8
8 - CTS - Clear To Send - Red looped to 7
9 - NC

### wires in multimeter end
Brown - R
Yellow - G
White - T
Green - Neg
Orange - Pos

### Standard RS232 D9
1 - DCD - Data Carrier Detect
2 - RXD - Recieve Data
3 - TXD - Transmit Data
4 - DTR - Data Terminal Ready
5 - GND - Signal Ground
6 - DSR - Data Set Ready
7 - RTS - Request to Send
8 - CTS - Clear To Send
9 - RI - Ring Indicator

pins required
2 - rx - YELLOW
5 - gnd - BLACK
4 - DTR - high - RED
7 - RTS - low - BLACK

## ON RS232
DTR to RTS - 6.95v
DTR to GND  - 13.47v

![](https://community.cisco.com/legacyfs/online/legacy/1/4/1/106141-RS232.png)