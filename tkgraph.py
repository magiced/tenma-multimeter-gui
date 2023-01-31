import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk )
from matplotlib.figure import Figure
import tkinter as Tk
import tkinter.ttk as ttk
import random
import time
import easyfiledialogs

# https://matplotlib.org/stable/api/backend_tk_api.html#matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
"""
TODO

* [x] modify update code to work with my data
* [x] DONE - add graph title/ axis labels
* [x] - work out why titles etc are not given space in canvas widgets
* [x] - add second/more graphs
* add second line 
* [x] - move update function into class (think this may solve update problem)
* [x] clean up update function
* [x] add start and stop graph functions for connecting to buttons
* [x] autoscale y, possible also x
* [ ] add 'start graph' function to make first call clearer to user
* [ ] add input cleaning to check for unplottable/garbage data
* [ ] could autoscale x be used to re-scale the x axis. i.e. it will change to 
        fit the number of values in the dataset plotted. so you could chane the 
        size of the dataset to change the graph width. i.e. change from 60 rows to 
        3600 rows. you'd generate x lines of [time, 0], then add the existing data
        at the end to 

* [ ] change graph size function
* [ ] reset graph function    
"""

# class GraphSeries(series_name=''):
#     def __init__(self):
#         self.x_data = []
#         self.y_data = []
#         self.name = self.series_name

#     def add_value(self, x_val, y_val):
#         self.x_data.append(x_val)
#         self.y_data.append(y_val)

#     def clear_series(self):
#         self.x_data = []
#         self.y_data = []

#     def get_series_name(self):
#         return self.name
    
"""
other functions
pop
len (is there a way of doing a proper len? don't make your life difficult ed...
set_max_width
change max width

"""


class tkGraph(Tk.Frame):
    def __init__(self,parent, **kwargs, ):
        Tk.Frame.__init__(self,parent,**kwargs)

        self.x_data = []
        self.y_data = []

        self.max_y_value = 0
        self.min_y_value = 0
        self.max_x_value = 0
        self.min_x_value = 0

        self.traces = dict()
        self.b_running = True

        self.not_new_line = False

        self.autoscale_y_on = False
        self.autoscale_x_on = False

        # Define matplotlib figure
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_tight_layout(True)
        self.ax.autoscale(tight=False)
        # self.ax.set_ylim(34,46)
        
        # self.ax.set_xlim()

        # self.ax.legend()

        # Tell Tkinter to display matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw() # show() - show does not work for this

    """ Tkinter layout methods """    
    def grid(self, **kwargs):#row, column):
        self.canvas.get_tk_widget().grid(kwargs)#row=row,column=column)#, side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def pack(self, **kwargs):
        self.canvas.get_tk_widget().pack(kwargs)#(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    """" graph format methods """

    def set_xlabel(self, label, **kwargs):
        self.ax.set_xlabel(label, kwargs)
        pass

    def set_ylabel(self, label, **kwargs):
        self.ax.set_ylabel(label, kwargs)
        pass

    def set_title(self, title, **kwargs):
        self.ax.set_title(title, kwargs)
        pass

    def set_color(self,color):
        # self.ax.line1.set_color(color)
        pass

    def set_grid_lines(self, visible=None, which='major', axis='both', **kwargs):
        self.ax.grid(visible, which, axis, **kwargs) # color = 'tab:gray', linestyle='-', linewidth=1)

    def set_bg_color(self, color):
        self.ax.set_facecolor(color)

    """ Graph use methods """

    def reset_graph(self):
        self.reset_y_max_min()

    def toggle_graph(self):
        """ toggles the graph running bool """
        if self.b_running == True:
            self.b_running = False
        elif self.b_running == False:
            self.b_running = True

    def get_graph_running_state(self):
        """ returns the running state """
        return self.b_running

    def start_graph(self):
        self.b_running = True
        """if graph has been paused, restart it""" 
        pass

    def pause_graph(self):
        self.b_running = False
        """ if graph is running, stop it where it is, but keep the data """

    def save_graph(self,filename):
        """ opens a filedialog to choose a save place and filename, and then saves
        a png of the graph """
        # self.pause_graph()

        # # get filename using my save dialog library
        # filename = './savetest.png'
        self.fig.savefig(filename, dpi=200) # use fig save f.savefig(filename.parent / (filename.stem +  '.png'),dpi=200)
        # self.start_graph()
        pass

    def set_graph_x_width(self, width):
        """ method to set the graph width, used for resetting and increasing the 
        amount of data displayed on the graph """
        self.x_width = width
        pass

    def set_autoscale_y_on(self):
        self.autoscale_y_on = True

    def set_autoscale_y_off(self):
        self.autoscale_y_on = False
    
    def set_autoscale_x_on(self):
        self.autoscale_x_on = True

    def set_autoscale_x_off(self):
        self.autoscale_x_on = False

    """ Methods for setting data """

    # this code is for a multiple line graph, but i havent got it working yet
    # def update_graph(self,name,dataset_x,dataset_y):
    #     if name in self.traces:
    #         self.line.set_data(dataset_x,dataset_y)
    #         # print(f'{name}, {dataset_x[0]}, {dataset_y[0]}')
    #     else:
    #         self.traces[name] = True
    #         self.line, = self.ax.plot(dataset_x,dataset_y,label=name)
    #     self.canvas.draw()

    def update_graph(self,dataset_x,dataset_y):
        """ directly sets the graph, using either external data or the classes'
        internal x_data and y_data variables if called by the graph_update_timer method"""

        if self.b_running:
            if self.not_new_line: # if it's not a new line
                self.line.set_data(dataset_x,dataset_y)
                self.update_y_max_min(dataset_y)                
                self.ax.set_ylim(self.min_y_value - abs(0.2*self.min_y_value), self.max_y_value + 0.2*self.max_y_value) # don't need to resize x axis, as this is controlled by the dataset width
                self.ax.axes.relim() # redraws the axes to account for any change in limits
                self.ax.autoscale_view()

            else: # if it is a new line
                self.not_new_line = True
                self.line, = self.ax.plot(dataset_x,dataset_y) # draw the new line
        self.canvas.draw()

    def set_graph_data(self, x_data, y_data):
        """ sets graph data so the graph can be updated seperately using the 
        graph_update_timer method"""
        self.x_data = x_data
        self.y_data = y_data

    def update_y_max_min(self, this_y_data):
        # update max y
        if len(this_y_data) > 2:
            # print('update')
            if (max(this_y_data) > self.max_y_value):
                # print('max update')
                self.max_y_value = max(this_y_data)

            if (min(this_y_data) < self.min_y_value):
                # print('min update')
                self.min_y_value = min(this_y_data)

        elif len(this_y_data) <= 2:
            # print('set')
            self.max_y_value = this_y_data[0]
            self.min_y_value = this_y_data[0]
        # else:
        #     print('pass')
        #     pass

        # print(f'max x: {self.max_y_value}, min x: {self.min_y_value}, {max(this_y_data)}, {min(this_y_data)}')  
        # 
    def reset_y_max_min(self):
        self.max_y_value = self.min_y_value      # note, this is a dirty hack until i rearrrange how the library handles data 

    def update_x_max_min(self):
        # update max x vals
        if (len(self.x_data) > 0):
            if max(self.x_data) > self.max_x_value:
                self.max_x_value = max(self.x_data)

            if min(self.x_data) < self.min_x_value:
                self.min_x_value = min(self.x_data)
        else:
            pass
    
    def graph_update_timer(self, update_period):
        """ periodically updates the graph using the data set seperately"""
        self.update_graph(self.x_data,self.y_data)
        root.after(update_period,self.graph_update_timer,update_period)      



if __name__=="__main__":

    def create_sin_curve(phase):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t + phase)
        phase += 0.1
        # self.update_graph("test",t,s)
        return phase, [t,s]

    def create_random_test_data( length, min=0, max=10 ):
        rand_x = [i for i in range(length)]
        rand_y = [random.randint( min , max ) for i in range(length)]
        # del rand_y[0]
        # rand_y.append(random.randint(0,10))
        return rand_x, rand_y

    def pause_button_clicked():
        plot.toggle_graph()
        if plot.get_graph_running_state() == True:
            button1['text'] = 'PAUSE'
        else:
            button1['text'] = 'START'

    def main_loop():
        global phase
        global sin_data

        phase, sin_data = create_sin_curve(phase)
        rand_x, rand_y = create_random_test_data(10, min=-1000, max=1000)

        plot.set_graph_data(rand_x, rand_y) #.set_graph_data(sin_data[0], sin_data[1])
        # plotB.set_graph_data(rand_x, rand_y)

        # # changes background color based on max value, for an alert
        # if max(rand_y) >= 10:
        #     plotB.set_bg_color('red')
        #     print('RED')
        # else:
        #     plotB.set_bg_color('green')
        # # plot.update_graph(sin_data[0], sin_data[1])
        # # plotB.update_graph(rand_x, rand_y)

        root.after(50, main_loop)


    root = Tk.Tk()

    plot = tkGraph(root)
    # plotB = tkGraph(root)
    plot.set_xlabel('time')

    # plotB.set_title('random line')
    # plotB.set_ylabel('RANDOM')
    # plotB.set_color('red')
    plot.set_grid_lines(color='navy', axis='x')
    # plotB.set_grid_lines(color='black', axis='y')
        
    button1 = Tk.Button(root,text='PAUSE', command=pause_button_clicked)
    button2 = Tk.Button(root, text='START')#, command=plot.start_graph)
    
    plot.grid(row=0,column=0)
    # plotB.grid(row=1,column=0)
    button1.grid(row=0,column=1)
    button2.grid(row=1,column=1)
    
    sin_data = [ [] , [] ]

    phase = 0
    rand_x = [i for i in range(10)]
    rand_y = [0 for i in range(10)]

    main_loop()
    plot.graph_update_timer(200)
    # plotB.graph_update_timer(200)

    root.mainloop()