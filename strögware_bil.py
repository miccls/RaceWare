'''
To do:

Fixa GPS info så att man vet när man kört ett varv, lagra detta i en dict som man sedan kan skicka över med 
allt annat godis. Denna dict ska innehålla den info som syns i depot varianten. Lagra i JSON och spara även ner 
en kopia av denna när man stänger ner programmet. Både när man trycker på q och när man trycker på stop. Kolla om det 
redan finns en och om det gör det, byt namn och spara sedan. Gör även en .py fil som samlar depot och bil-varianterna
och frågar vilken man vill köra. 

-------------------------------------------------------------------------------------

För medlemmar i storströgarna som är inne på sightseeing::

Kommentarer # ...
De är skrivna i engelska om de är är för att stanna,
annars i svenska. Det är schysst med engelska kommentarer om
man ska inkludera detta arbete i någon slags portfolio.
Här, i denna fil kommer to do listan uppdateras och ni kan 
följa arbetet på github.com/miccls/Str-gware där det kommer uppdateras
frekvent.

Vissa ställen markerar även VScode som rött för att den inte ser att pygame
har de attribut som jag använder. Eftersom dessa är attribut i klasser 
som finns inne i pygame modulen så tror den att de inte finns så de 
som än så länge är rödmarkerat kan man bara ignorera.
'''


import tkinter as tk
import tkinter.ttk as ttk
from settings import Settings
from tracks import Tracks
from position import Position
from PIL import Image, ImageTk
import time
import json
import gpiozero
import requests
from time import sleep
from os import sys
from gauges import Gauges
from shiftlight import Shiftlight
from rich.traceback import install
# Tills jag vet att allt fungerar.
try:
    from obd_com import OBDII
except:
    pass

class strögware_bil:

    def __init__(self):
        # Ett test av rich:s felhantering konsollmanipulering
        install()
        # En inställning för att justera inställningar rätt
        in_car = True
        # Hämtar de tillgängliga inställningarna.
        self.settings = Settings(in_car)
        # Hämtar all tillgänglig ban-info.
        self.tracks = Tracks(self)
        # Flag för testning av programmet.
        self.counting = False
        self.update_counter = 0
        # Kommandon som bilen ska läsa.
        self.command_list = {
    	    'rpm' : 'RPM',
 			'km/h' : 'SPEED',
            'throttle' : 'THROTTLE_POS',
            'water' : 'COOLANT_TEMP',
            'oiltemp' : 'OIL_TEMP',
            'load' : 'ENGINE_LOAD'
        }

        self.measurements_dict = {}

        # Allmän info om mätarna. Ifall det ska multipliceras med något, lägg in det 
        # i gauges - klassen. Typ if unit == '%': value *= 100.
        self.gauges_info = {
            'rpm' : {'unit' : None, 'upper_limit' : 8000},
 			'kmh' : {'unit' : None, 'upper_limit' : None}, 
            'throttle' : {'unit' : '%', 'upper_limit' : None},
            'water' : {'unit' : '°', 'upper_limit' : 110},
            'oiltemp' : {'unit' : '°', 'upper_limit' : 180},
            'load' : {'unit' : 'hp', 'upper_limit' : None}
            }

        try: 
            self.obd_instance = OBDII(self, self.command_list)
            self.settings.obd_active = True
        except:
            pass

        # Använder Tkiner för att ställa in 
        # skärmen och startförhållanden.
        self._init_screen()
        requests.put(self.settings.base_url + "location/gps", {"lat" : 0, "lon" : 0})


    def _init_screen(self):

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.settings.screen_width = self.root.winfo_screenwidth()
        self.settings.screen_height = self.root.winfo_screenheight()
        self.root.bind('<Key>', self._key_pressed)
        self.canvas = tk.Canvas(self.root,
            height = self.settings.screen_height,
            width = self.settings.screen_width,
            bg = self.settings.bg_color)
        self.canvas.pack()
        self.buttonframe = tk.Frame(self.canvas,
            bg = '#f5d742')
        self.buttonframe.place(relx = 0.5, rely = 0.5,
            anchor = 'center')
        self.button1 = tk.Button(self.buttonframe,
            bg = '#000000', highlightcolor = '#ffffff',
            text = 'Mantorp',
            width = 10,
            height = 2)
        button_dict = {}
        for key in self.tracks.tracks_dict.keys():
            button_dict[key] = tk.Button(self.buttonframe,
            bg = self.settings.button_color,
            text = key.title(),
            width = 15,
            height = 2,
            command = lambda track = key: self._init_track(track))   
            button_dict[key].pack()
    
    def _check_state(self):
        if self.settings.track_available:
            self._update_pos()
        self._update_values()
        self._update_screen()
        if self.update_counter >= 15:
            try:
                self._send_data()
            except: 
                print("Ingen anslutning")
        self.root.after(self.settings.delay_time,self._check_state)

    def _update_screen(self):
        if self.counting:
            self.update_counter += 1
            for value in self.gauge_dict.values():
                if value.value < 8300:
                    value.value += 20
                else:
                    value.value = 0
                value.give_gauge_value()
            self.shiftlight.update_colors(
                self.gauge_dict['rpm'].value)
        # Räkna varvtid. 
             # Kolla här så att allt är ok.
             # Se till så att _format_time används i 
             # _update_pos()!
        self._update_pos()


    def _format_time(self):
        '''Formatterar ett antal sekunder'''
        # Här får jag fixa så att det blir fint.
        display_time = time.time() - self.gps_pos.start_time
        decimals = display_time - round(display_time - 0.5)
        # Tar fram hundradelar
        hundreds = round(decimals*100 - 0.5)
        seconds = round(display_time - 0.5)
        minutes = round((seconds/60) - 0.5)
        seconds -= minutes*60
        display_time = f"{minutes}:{seconds}:{hundreds}"
        return display_time
            
    def _update_pos(self):
        '''Uppdaterar punkten på kartan'''
        # Nästa steg är att nolla den när man ser att det funkar.
        try:
            if self.gps_pos.counter:
                lat, lon = self.gps_pos.get_pos()
                self.gps_data = {"lat" : lat, "lon" : lon}
                print(self.gps_data)
                self._send_data('gps_data')
        except:
            pass

    def _key_pressed(self, event):
        print(event.char)
        if event.char == 'c':
            if self.counting:
                self.counting = False
            else:
                self.counting = True
        if event.char == 'q':
            sys.exit()

        if event.char == 's':
            lat, lon = self.gps_pos.get_pos()
            self.gps_data = {"lat" : lat, "lon" : lon}
            print(self.gps_data)
            self._send_data('gps_data')
            self._send_data('gauge_data')
            # Experiment för att skicka data

    def _send_data(self, measurement):
        '''Metod som lagrar data i databas på FLASK REST-API'''
        # Denna används för att det är min dators lokala ip.
        base_url = "http://192.168.1.129:5000/"
        # Kopierar mätarnas värden och lägger i ett dictionary som sedan
        # skickas med id data1.
        if measurement == 'gauge_data':
            for key, value in self.gauge_dict.items():
                self.measurements_dict[key] = value.value
            print(self.measurements_dict)
            response = requests.patch(base_url + "measurements/data1", self.measurements_dict)
        elif measurement == 'gps_data':
            response = requests.patch(base_url + "location/gps", self.gps_data)
            print(response)


    def run(self):
        self._update_screen()
        self.root.mainloop()

    def _init_track(self,track):

        # När en bana blivit vald körs koden i denna metod.
        # Tar bort listan med knappar.
        self.buttonframe.destroy()
        self.track_dict = self.tracks.tracks_dict[track]

        if track in self.tracks.image_dict.keys():
            
            # Lägg ut position på kartan.
            self.gps_pos = Position(self, self.canvas,)
            self.gps_pos.draw_clock(0.40, 0.3, 'nw')
            self.settings.track_available = True
        else:
            # Det finns ingen bild, skriv ut ett meddelande på skärmen.
            self.no_picture_label = tk.Label(self.canvas, 
                text = self.settings.no_image_text, font=(self.settings.gauge_font,
				self.settings.gauge_font_size,),
                bg = self.canvas['background'],
                fg = 'white')
            self.no_picture_label.place(x=self.settings.screen_width * 0.75,
                y=self.settings.screen_height * 0.75,
                anchor = 'center',)

        self.start_count_button = tk.Button(self.canvas, text = "Start", 
            fg = self.settings.green_color, 
            command = lambda: self._toggle_measurements()) 
        # rely = 0.15 linjerar i överkant med shiftlighten.
        self.start_count_button.place(relx = 0.9, rely = 0.15, anchor = 'ne')

        # Fixa mätare.
        self._init_gauges()
        self.shiftlight = Shiftlight(self, self.canvas)
        self._check_state()

    def _toggle_measurements(self):
        self.gps_pos.start_count(self)
        if self.counting:
                self.counting = False
        else:
            self.counting = True
        

    def _init_gauges(self):
        ''' Lägger ut mätarna på skärmen '''
        self.gauge_frame = tk.Frame(self.canvas, bg = self.canvas['background'],
            width = self.settings.screen_width * self.settings.gauge_frame_width,
            height = self.settings.screen_height * self.settings.gauge_frame_height)
        self.gauge_frame.place(relx = self.settings.gauge_pos_x, rely = self.settings.gauge_pos_y, 
            anchor = self.settings.gauge_anchor,)
        self.gauge_dict = {}
        # Placerar ut knappen.
        rely = 0.5
        relx = 0.25
        for key in self.gauges_info.keys():
            # Om den ska ha enhet, ge den en. Annars låt bli
            if self.gauges_info[key]['unit']:
                self.gauge_dict[key] = Gauges(self.gauge_frame, 
                    main = self,
                    label_text = key,
                    unit = self.gauges_info[key]['unit'],
                    upper_limit = self.gauges_info[key]['upper_limit'])
            else:
                self.gauge_dict[key] = Gauges(self.gauge_frame, 
                    main = self, 
                    label_text = key)
            if key in self.settings.car_gauges:
                self.gauge_dict[key].show_gauge(type = 'place', relx = relx, rely = rely, anchor = 'center')
                relx += 0.25

        
    # Ahhhhhhh de godis.

    def _update_values(self):
        # Lagra uppdatera värden i gauges.
        try: # Detta för att jag inte fixat med OBDII än.
            for key, value in self.gauge_dict.items():
                value.value = self.obd_instance.get_value(key)
                value.give_gauge_value()
        except AttributeError:
            pass

        



        


if __name__ == '__main__':
    strög = strögware_bil()
    strög.run()

