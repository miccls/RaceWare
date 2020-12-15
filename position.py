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

    def init_GPS(self):
        '''Initierar GPS port vald i settings.py.'''
        mport = "/dev/ttyAMA0"
        self.ser = serial.Serial(mport,9600,timeout = 1)

    def get_pos(self):
        new_data = False
        # Om vi lyckats läsa data
        while not new_data:
            try:
                data = self.ser.readline().decode()
            except:
                pass
            else:
                new_data = True

        lat, lon = self._parseGPS(data)
        print(lat,lon)
        return lat, lon


    def draw_clock(self, relative_x, relative_y, anchor):
        # Fixa varvtidsklockan.
        self.lap_time_label = tk.Label(self.master, text = '0:0:0',
            font = (self.settings.timer_font, self.settings.timer_font_size),
            fg = 'white',
            bg = self.master['background'],)
        # Placerar trevligt under shiftlighten. relx = 0.4 rely = 0.3 anchor nw
        self.lap_time_label.place(relx = relative_x, rely = relative_y, anchor = anchor)





    def _parseGPS(self, data):
        if data[0:6] == "$GPGGA":
            s = data.split(",")
            if s[7] == '0' or s[7]=='00':
                print ("no satellite data available")
                return
            lat = decode(s[2])
            lon = decode(s[4])
            return  lat,lon
    


    def _decode(self, coord):
        l = list(coord)
        for i in range(0,len(l)-1):
                if l[i] == "." :
                        break
        base = l[0:i-2]
        degi = l[i-2:i]
        degd = l[i+1:]
        #print(base,"   ",degi,"   ",degd)
        baseint = int("".join(base))
        degiint = int("".join(degi))
        degdint = float("".join(degd))
        degdint = degdint / (10**len(degd))
        degs = degiint + degdint
        full = float(baseint) + (degs/60)
        #print(full)
        
        return full
