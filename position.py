import time
import tkinter as tk
import serial
import pynmea2

class Position:

    def __init__(self,main,master):
        '''Initierar GPS-punkten och varvtidsklockan'''
        self.master = master
        self.settings = main.settings
        # För att kunna modifiera objekt på huvudcanvasen.

        # Port för seriell kommunikation med GPS - enhet.
        self.port = self.settings.GPS_port

        self.counter = False
        self.start_time = 0

    
        #self._init_GPS()

    def move(self, x0, y0):
        '''Flytta bilens GPS-punkt.'''
    
        # Funktion i tkinter som ändrar koordinaterna på objekt på canvas.
        self.master.coords(self.pointer, x0, y0,
            x0 + self.settings.pos_point_radius,
            y0 + self.settings.pos_point_radius)

    def draw_pointer(self):
        self.pointer = self.master.create_oval(0,
            0,
            self.settings.pos_point_radius,
            self.settings.pos_point_radius,
            fill = self.settings.red_color)
        
        self.move(100,100)

    def start_count(self, main):
        self.counter = not self.counter
        if self.counter:
            self.start_time = time.time()
            main.start_count_button.config(text = 'Stop',
                fg = self.settings.red_color)
        else: 
            main.start_count_button.config(text = 'Start',
                fg = self.settings.green_color)

    def _init_GPS(self):
        '''Initierar GPS port vald i settings.py.'''
        self.ser = serial.Serial(self.port, baudrate = 9600, timeout = 0.5)
        data_out = pynmea2.NMEAStreamReader()

    def get_pos(self):
    #     new_data = self.ser.readline()
    #     while new_data[0:6] != '$GPGLL':
    #         new_data = self.ser.readline()
    #     new_msg = pynmea2.parse(new_data)
    #     lat = new_msg.latitude
    #     lon = new_msg.longitude
    #     return lat, lon
        return 1

    def draw_clock(self, relative_x, relative_y, anchor):
        # Fixa varvtidsklockan.
        self.lap_time_label = tk.Label(self.master, text = '0:0:0',
            font = (self.settings.timer_font, self.settings.timer_font_size),
            fg = 'white',
            bg = self.master['background'],)
        # Placerar trevligt under shiftlighten. relx = 0.4 rely = 0.3 anchor nw
        self.lap_time_label.place(relx = relative_x, rely = relative_y, anchor = anchor)


    def set_pos(self, position):
        pass