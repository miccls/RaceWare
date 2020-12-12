'''
To do:

Lägg in alla grafiska element som kan vara bra. Nu är mätarvärden och varvtidsdata inne.
Kanske ha med genomsnittsdata eller liknande. Annars: Fixa om kartan så att den är i fokus.
Lägg den mot mitten och lös överföring av gpsdata via APIN från bilen hit.

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
# Tills jag vet att allt fungerar.
try:
    from obd_com import OBDII
except:
    pass

class tkinterströg:

    def __init__(self):
        # En inställning för att justera inställningar rätt
        self.in_car = False
        # Hämtar de tillgängliga inställningarna.
        self.settings = Settings(self.in_car)
        # Hämtar all tillgänglig ban-info.
        self.tracks = Tracks(self)
        # Flag för testning av programmet.
        self.counting = False
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

        # Varvdata specificeras i denna dict.
        self.lap_data = {
            'antal' : 0,
            'senaste' : 'N/A',
            'bästa' : 'N/A',
            }

        # Använder Tkiner för att ställa in 
        # skärmen och startförhållanden.
        self._init_screen()


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

    # Funktion som löper kontinuerligt. Den har en tid efter vilken den kör.
    # I inställningar kan man modifiera denna tid.
    
    def _check_state(self):
        if self.settings.track_available and self.in_car:
            self._update_pos()
        self._update_values()
        self._update_screen()
        self.root.after(self.settings.delay_time,self._check_state)

    def _update_screen(self):
        if self.counting:
            # Hämtar data från enheten i bilen.
            try:
                temp_dict = self._get_data()
            except:
                print("Anslutnings problem. Connection refused.")
            else:
                for key, value in temp_dict.items():
                    self.gauge_dict[key].value = value

                for value in self.gauge_dict.values():
                    value.give_gauge_value()

        # Räkna varvtid.
        try:
            if self.gps_pos.counter: 
             # Kolla här så att allt är ok.
             # Se till så att _format_time används i 
             # _update_pos()!
                self._update_pos()
        except AttributeError:
            pass 


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
        if self.gps_pos.counter:
            self.gps_pos.lap_time_label.config(text = self._format_time())

    def _key_pressed(self, event):
        print(event.char)
        if event.char == 'c':
            if self.counting:
                self.counting = False
            else:
                self.counting = True
        if event.char == 'q':
            sys.exit()

        if event.char == 'g':
            self._update_screen()

            # Experiment för att skicka data

    def _send_data(self):
        '''Metod som lagrar data i databas på FLASK REST-API'''
        # Denna används för att det är min dators lokala ip.
        base_url = "http://192.168.1.129:5000/"
        # Kopierar mätarnas värden och lägger i ett dictionary som sedan
        # skickas med id data1.
        for key, value in self.gauge_dict.items():
            self.measurements_dict[key] = value.value
        print(self.measurements_dict)
        response = requests.patch(base_url + "measurements/data1", self.measurements_dict)

    def _get_data(self):
        base_url = "http://192.168.1.129:5000/"
        response = requests.get(base_url + "measurements/data1")
        response = response.json()
        # Skickar ut data utan id.
        del response["id"]
        return response


    def run(self):
        self._update_screen()
        self.root.mainloop()

    def _init_track(self,track):

        # När en bana blivit vald körs koden i denna metod.
        # Tar bort listan med knappar.
        self.buttonframe.destroy()
        self.track_dict = self.tracks.tracks_dict[track]

        if track in self.tracks.image_dict.keys():
            #Sätt bildflaggan till true.
            self.track_image = self.tracks.get_image(track)
            self.image_canvas = tk.Canvas(self.canvas,
                height = self.track_image.height(),
                width = self.track_image.width(),
                bg = self.canvas['background'],
                highlightthickness=0)  # Fixa denna canvas så man kan lägga in en punkt.
            self.image_canvas.place(
                x=self.settings.screen_width * 0.75,
                y=self.settings.screen_height * 0.75,
                anchor = 'center',
                )
            self.image_canvas.create_image(
                0,
                0,
                anchor = 'nw', 
                image = self.track_image)
            # Lägg ut position på kartan.
            self.gps_pos = Position(self, self.canvas)
            self.gps_pos.draw_clock(0.45, 0.3, 'nw')
            self.gps_pos.draw_pointer()
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
        


        # Fixa countknappen, det gör jag hellre här än i positionklassen

        self.start_count_button = tk.Button(self.canvas, text = "Start", 
            fg = self.settings.green_color, 
            command = lambda x = self: self.gps_pos.start_count(x))
        # rely = 0.15 linjerar i överkant med shiftlighten.
        self.start_count_button.place(relx = 0.9, rely = 0.15, anchor = 'ne')

        # Fixa mätare.
        self._init_gauges()
        # Visa varv data:
        self._init_lap_data()
        #self.shiftlight = Shiftlight(self, self.canvas)
        self._check_state()


    def _init_lap_data(self):
        ''' Skapar visare för varvdata '''
        self.lap_frame = tk.Frame(self.canvas, bg = self.canvas['background'],
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
                main = self, 
                label_text = key)
            self.lap_info_gauges[key].value = value
            self.lap_info_gauges[key].show_gauge(type = 'grid',row = row, column = column)
            self.lap_info_gauges[key].give_gauge_value()
            row += 1
            if row == 4:
                row = 1
                column += 1


    #################################################
        


    def _init_gauges(self):
        ''' Lägger ut mätarna på skärmen '''
        self.gauge_frame = tk.Frame(self.canvas, bg = self.canvas['background'],
            width = self.settings.screen_width * self.settings.gauge_frame_width,
            height = self.settings.screen_height * self.settings.gauge_frame_height)
        self.gauge_frame.place(relx = self.settings.gauge_pos_x, rely = self.settings.gauge_pos_y, 
            anchor = self.settings.gauge_anchor,)
        self.gauge_dict = {}
        # Lägger till knapp för att ändra mätare.
        self.gauge_button = tk.Button(self.gauge_frame,
            bg = self.settings.button_color, highlightcolor = self.settings.button_color,
            text = 'Ändra',
            width = 10,
            height = 2,
            command = lambda: self._gauge_menu())
        # Placerar ut knappen.
        self.gauge_button.grid(row = 0, column = 0)
        row = 1
        column = 0
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
            self.gauge_dict[key].show_gauge(type = 'grid', row = row, column = column)
            row += 1
            if row == 4:
                row = 1
                column += 1
        
    # Ahhhhhhh de godis.


    def _gauge_menu(self):
        '''Meny för att välja vilka mätare som ska visas.'''
        for widget in self.gauge_frame.winfo_children():
            widget.destroy()
        for gauge in self.gauge_dict.values():
            gauge.tklabel.destroy()
            del gauge
        # Placera högst upp i framen.
        tk.Label(self.gauge_frame, text = "Välj mätare: ",
            bg = self.canvas['background'],
            fg = 'white',
            font = (self.settings.gauge_font,
				self.settings.gauge_font_size,)).grid(row = 0, column = 0)
        # Sätt ut valmöjligheter
        self.check_box_dict = {}
        self.check_box_variables = {}
        count = 1
        row = 0
        column = 0
        for key in self.gauges_info.keys():
            # För att placera ut i kolumner om 3 element.
            row += 1
            if row == 4:
                row = 1
                column += 1
            self.check_box_variables[key] = tk.BooleanVar()
            self.check_box_dict[key] = tk.Checkbutton(self.gauge_frame, text = key.title(),
                takefocus = 0, variable = self.check_box_variables[key],
                bg = self.canvas['background'], fg = '#ffffff',
                height = 2, width = 15,
                font = (self.settings.gauge_font, self.settings.gauge_font_size))
            self.check_box_dict[key].grid(row = row, column = column)
            
            count += 1  # Fortsätt här, knapparna ska ut och längst ner ska knapp som säger välj, när den trycks så gå vidare.
        # Knapp för att bekräfta val
        self.confirm = False
        self.confirm_button = tk.Button(self.gauge_frame,
            bg = self.settings.button_color, highlightcolor = '#ffffff',
            text = 'Bekräfta',
            width = 10,
            height = 2,
            command = (lambda: self._confirm()))
        self.confirm_button.grid(row = row + 1, column = column)

    def _confirm(self):
        # Vad som ska hända när knappen är tryckt.
        for widget in self.gauge_frame.winfo_children():
            widget.destroy()
        for key in self.check_box_dict.keys():
            self.check_box_dict[key].destroy()
        # Lägg ut ny knapp.
        self.gauge_button = tk.Button(self.gauge_frame,
            bg = '#000000', highlightcolor = '#ffffff',
            text = 'Ändra',
            width = 10,
            height = 2,
            command = lambda: self._gauge_menu())

        self.gauge_button.grid(row = 0, column = 0)
        row = 1
        column = 0
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

            if self.check_box_variables[key].get():    
                row += 1
                if row == 4:
                    row = 1
                    column += 1    
                self.gauge_dict[key].show_gauge(type = 'grid', row = row, column = column)



        
            

        # Funktion som uppdaterar värden.
        if self.settings.obd_active:
            self._update_values()


    def _update_values(self):
        # Lagra uppdatera värden i gauges.
        try: # Detta för att jag inte fixat med OBDII än.
            for key, value in self.gauge_dict.items():
                value.value = self.obd_instance.get_value(key)
                value.give_gauge_value()
        except AttributeError:
            pass

        



        


if __name__ == '__main__':
    strög = tkinterströg()
    strög.run()

