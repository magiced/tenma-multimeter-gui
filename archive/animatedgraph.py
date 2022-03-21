from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

""" references:
https://gist.github.com/Overdrivr/48e2c679cf238d7214a3
Github: https://gist.github.com/electronut/d5e5f68c610821e311b0


"""


class animatedGraph():
    def __init__(self):
        #what do i have to intialise here to make this work nicely?
        self.list_length = 30 # need to have the user set this as part of the initial call
        # but also it needs to change if the graph width changes
        self.fifo_list = [0] * self.list_length

    def update_graph(self, latest_value):
        self.new_val = latest_value

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
                fifo_list = fifo(self.fifo_list, self.new_val)
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

if __name__ = '__main__':
    pass
    # create a test graph using random np data