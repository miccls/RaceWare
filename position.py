import time
import tkinter as tk

class Position:

    def __init__(self,main,master):
        '''Initierar GPS-punkten och varvtidsklockan'''
        self.master = master
        self.settings = main.settings
        # Om vi har börjat tidtagning.
        self.counter = False

        # Fixa varvtidsklockan.
        self.lap_time_label = tk.Label(main.canvas, text = '00:00:00',
            font = (self.settings.timer_font, self.settings.timer_font_size),
            fg = 'white',
            bg = main.canvas['background'],)
        self.lap_time_label.place(relx = 0.5, rely = 0.4, anchor = 'center')

        # Skapar punkten.
        self.pointer = master.create_oval(0,
            0,
            self.settings.pos_point_radius,
            self.settings.pos_point_radius,
            fill = self.settings.red_color)
        
        self.move(100,100)

        self._init_GPS()

    def move(self, x0, y0):
        '''Flytta bilens GPS-punkt.'''
    
        # Funktion i tkinter som ändrar koordinaterna på objekt på canvas.
        self.master.coords(self.pointer, x0, y0,
            x0 + self.settings.pos_point_radius,
            y0 + self.settings.pos_point_radius)

    def start_count(self, bool):
        self.counter = bool
        if bool:
            self.start_time = time.time()
        else: 
            self.start_time = 0

    def _init_GPS(self):
        pass

    def get_pos(self):
        pass