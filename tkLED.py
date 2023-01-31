# import time
# import datetime
import tkinter as tk
# import tkinter.ttk as ttk

class LED(tk.Label):
    def __init__(self, parent, on_colour='red', off_colour='black', initial_state=False, **kwargs, ):
        # tk.Label.__init__(self, parent, **kwargs)
        self.on_colour = on_colour
        self.off_colour = off_colour
        self.state = False

        self.led = tk.Label(parent, text='   ', bg=self.off_colour, justify='center', relief='solid', borderwidth=2, padx=5, pady=5, font=('bold'))

        # print(f"Initial State {self.on_colour}: {self.state}")
        state_now = self.get_led_state()
        # print(state_now)
        self.set_led_state(state_now)

    """ set background colour """
    def set_bg_color(self, color):
        self.led['bg'] = color

    """ Tkinter layout methods """    
    def grid(self, **kwargs):#row, column):
        self.led.grid(kwargs)#row=row,column=column)#, side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def pack(self, **kwargs):
        self.led.pack(kwargs)#(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def lift(self, target):
        self.led.lift(target)
    
    """ Methods """

    def get_led_state(self):
        print(f"get state: {self.state}")
        return self.state

    def set_led_state(self, this_state):
        # print(f"Set State {self.on_colour}: {this_state}, {self.state}")
        if this_state:      # turn LED ON
            self.turn_on()
        else:               # turn LED OFF
            self.turn_off()
        # print(f"Set State {self.on_colour}: {self.state}")

    # ON
    def turn_on(self):
        self.set_bg_color(self.on_colour)
        self.state = True
        # print("turn on")

    # OFF
    def turn_off(self):
        self.set_bg_color(self.off_colour)
        self.state = False
        # print("turn off")

    # TOGGLE
    def toggle(self):
        if self.state:      # LED is ON
            self.turn_off()
            self.state = False
        else:               # LED is OFF
            self.turn_on()
            self.state = True
        # print(f"TOGGLE: {self.state}")
    # set value

if __name__ == "__main__":
    root = tk.Tk()

    red_led = LED(root)
    red_button = tk.Button(root, command=red_led.toggle)

    green_led = LED(root, on_colour='green')
    green_button = tk.Button(root, command=green_led.toggle)

    red_led.pack()
    red_button.pack()
    green_led.pack()
    green_button.pack()

    root.mainloop()