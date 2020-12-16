# Klass som innehåller funktioner som sköter varvdata.
import tkinter

import time
import tkinter as tk
from gauges import Gauges

class LapTimer:

    def __init__(self, main, master):
        '''
        Denna klass håller kod som fixar med alla varvtidsdata.
        Den kommer uppdatera de mätare som visar den infon.
        '''
        # Varvdata specificeras i denna dict.
        self.lap_data = {
            'antal' : 0,
            'senaste' : 'N/A',
            'bästa' : 'N/A',
            }

        self.master = master
        self.settings = main.settings
        # För att kunna modifiera objekt på huvudcanvasen.

        # Port för seriell kommunikation med GPS - enhet.
        self.port = self.settings.GPS_port

        self.counter = False
        self.start_time = 0


    def init_lap_data(self, main):
        ''' Skapar visare för varvdata '''
        self.lap_frame = tk.Frame(self.master, bg = self.master['background'],
            width = self.settings.screen_width * self.settings.gauge_frame_width,
            height = self.settings.screen_height * self.settings.gauge_frame_height)
        self.lap_frame.place(relx = 0.05, rely = (0.05 + self.settings.gauge_frame_height),
            anchor = 'nw')

        self.lap_info_gauges = {}

        row = 1
        column = 0
        for key, value in self.lap_data.items():
            # Använd gauge-class
            self.lap_info_gauges[key] = Gauges(self.lap_frame, 
                main = main, 
                label_text = key)
            self.lap_info_gauges[key].value = value
            self.lap_info_gauges[key].show_gauge(type = 'grid',row = row, column = column)
            self.lap_info_gauges[key].give_gauge_value()
            row += 1
            if row == 4:
                row = 1
                column += 1

    def start_count(self, main):
        self.counter = not self.counter
        if self.counter:
            self.start_time = time.time()
            main.start_count_button.config(text = 'Stop',
                fg = self.settings.red_color)
        else: 
            main.start_count_button.config(text = 'Start',
                fg = self.settings.green_color)


    def draw_clock(self, relative_x, relative_y, anchor):
        # Fixa varvtidsklockan.
        self.lap_time_label = tk.Label(self.master, text = '0:0:0',
            font = (self.settings.timer_font, self.settings.timer_font_size),
            fg = 'white',
            bg = self.master['background'],)
        # Placerar trevligt under shiftlighten. relx = 0.4 rely = 0.3 anchor nw
        self.lap_time_label.place(relx = relative_x, rely = relative_y, anchor = anchor)