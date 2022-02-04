"""
ldr.py

Display analog data from Arduino using Python (matplotlib)

Author: Mahesh Venkitachalam
Website: electronut.in
Github: https://gist.github.com/electronut/d5e5f68c610821e311b0
"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constructor
  def __init__(self, strPort, maxLen):
      # open serial port
      self.ser = serial.Serial(strPort, 115200)

	#creating a buffer using the deque function for each data val
      self.ax = deque([0.0]*maxLen)
      self.ay = deque([0.0]*maxLen)
      self.az = deque([0.0]*maxLen)

      #maxLen is the number of values shown on the x axis of the graph
      self.maxLen = maxLen

  # add to buffer
	# i already have this function, but just using the list methods
	# my buffer goes right to left
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val) #add an element to the right side of the deque if the buffer length isn't full yet
      else:
	#new val goes to left, values fall out of the right side
	# in>>>>>>>>out
          buf.pop() #remove and return the rightmost element of the deque list
          buf.appendleft(val) # add an element to the left side of the deque

  # add data
  def add(self, data):
      assert(len(data) == 3) #assert() sets a test and if it fails throws an exception. used to test data/valid input
      self.addToBuf(self.ax, data[0]) #add the value data[0] to the ax deque
      self.addToBuf(self.ay, data[1])
      self.addToBuf(self.az, data[2])

  # update plot
  def update(self, frameNum, a0, a1, a2):
      try:
          line = self.ser.readline() #reads the transmission form the serial port
          data = [float(val) for val in line.split()] #creates a list 'data' with the float conversion of the string val in line.split. each of the values is changed from a string to a float in this line, it's a great use of a comprehension
          # print data
          if(len(data) == 3):
              self.add(data)
              a0.set_data(range(self.maxLen), self.ax) #sets the data for the graph, x as the range 1-100, y as the deque. i think this is the function i've been looking for for mine to work!
              a1.set_data(range(self.maxLen), self.ay)
              a2.set_data(range(self.maxLen), self.az)
      except KeyboardInterrupt:
          print('exiting')
      
      return a0, #and it returns only one of the plot objects

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
#   # create parser
#   parser = argparse.ArgumentParser(description="LDR serial")
#   # add expected arguments
#   parser.add_argument('--port', dest='port', required=True)

  # parse args
#   args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
#   strPort = args.port
  #strPort = 'COM15'
  strPort = '/dev/ttyUSB0'

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 500)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 500), ylim=(0, 1024)) #needs to be 256 for rgb
#   ax = plt.axes(xlim=(0, 500), ylim=(0, 256)) #needs to be 256 for rgb
#   ax = plt.axes(xlim=(0, 500), ylim=(-130, 130)) #for showing map

# three plot objects here, all on the same graph
# declared they'll be taking a list in
  a0, = ax.plot([], [], color='red') 
  a1, = ax.plot([], [], color='limegreen')
  a3, = ax.plot([], [], color='blue')
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a0, a1, a3),  
                                 interval=50)
#fargs is the additional arguments to pass to the func argument, in operation, only a0, is returned, but then a1 and a2 are also passed in because they're in fargs

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
