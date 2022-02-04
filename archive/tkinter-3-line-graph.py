# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html

import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# TODO
# change line list to line1 line2 line3 etc or maybe list of line objects

b_clear_list = False

def fifo(list_in, new_val):
    del list_in[0] #delete first in value
    list_in.append(new_val) #append new value to end
    return list_in

def init():  # only required for blitting to give a clean slate.
    for i in range(len(fifo_list)):
        line0.set_ydata([np.nan] * len(x) )
        line1.set_ydata([np.nan] * len(x) )
        line2.set_ydata([np.nan] * len(x))
    return line0,

def animate(i):
    global b_clear_list
    global fifo_list
    # this function updates the y data each time
    if b_clear_list:
        print('clear')
        b_clear_list = False
        fifo_list = [ [0]*list_length, [0]*list_length, [0]*list_length ]

    input_list = [slider_bar_1.get(), slider_bar_2.get(), random.randint(5,15)]

    lbl_var.set(f"{input_list[0]}\t{input_list[1]}\t{input_list[2]}")

    print(input_list)

    for i in range(len(fifo_list)):
        fifo_list[i] = fifo(fifo_list[i],input_list[i])
        print(fifo_list[i])

    line0.set_ydata(fifo_list[0])
    line1.set_ydata(fifo_list[1])
    line2.set_ydata(fifo_list[2])

    #line.set_ydata(fifo_list[i])
    # return plots
    return [line0, line1, line2]

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def clear_graph():
    global b_clear_list
    b_clear_list = True

list_length = 10

root = tk.Tk()
root.wm_title("an animated graph")

#generate starting data
fifo_list = [ [0]*list_length, [0]*list_length, [0]*list_length ]
print(fifo_list)
x = [i for i in range(list_length)]
plots = []
#create the figure
fig, ax = plt.subplots()

line0, = ax.plot(x, fifo_list[0], label = 'line0', color="red")
line1, = ax.plot(x, fifo_list[1], label = 'line1', color="green")
line2, = ax.plot(x, fifo_list[2], label = 'line2', color='blue')

ax.set_ybound(lower = 0, upper = 20) # sets limits of y axis
fig.legend()

#create the canvas
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw() # why is the canvas drawn here?
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

button = tk.Button(master=root, text="CLEAR GRAPH", command=clear_graph)
button.pack()

lbl_var = tk.StringVar()
lbl_var.set("start")
lbl = tk.Label(root, textvariable=lbl_var)
lbl.pack()

slider_bar_1 = tk.Scale(root, from_=0, to=20, orient=tk.HORIZONTAL)
slider_bar_1.pack()

slider_bar_2 = tk.Scale(root, from_=0, to=20, orient=tk.HORIZONTAL)
slider_bar_2.pack()

slider_bar_3 = tk.Scale(root, from_=0, to=20, orient=tk.HORIZONTAL)
slider_bar_3.pack()


# this calls the animate function every 100ms
# https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=500, blit=True)

root.protocol("WM_DELETE_WINDOW", _quit)
# when you click the X icon to close the window, this function is called
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm#protocols

tk.mainloop()
