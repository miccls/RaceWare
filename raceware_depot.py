'''
To do:

FRÄMST: Fixa encapsulation. Riktigt skakigt i detta projekt.
Vet inte hur väl alla klasser håller encapsulation-regler. Kan göra
vidare utveckling till en riktig plåga ifall det inte beaktas.

Sätt lap_time-labeln i samma frame som den andra lap-datan.

Fixa även en label som beskriver de olika framesen till mätare och varvdata.

Kolla vad som behöver lite refactoring. Jobba på encapsulation. Det kommer hjälpa
i och med att programmet växer större och större. Just nu är det ganska rörigt och alla
klasser är och rör i varandra. Det finns mycket "room for improvement".

För övrigt: Kolla på JSON-sparandet. Se till att man får varvdatan från API, se till
att API har en resurs för att skicka och ta emot varvdata. I den metoden ska även lite
statistik kunna byggas med numpy för att visualisera ett race. Sist och kanske minst också,
städa upp rent GUI - mässigt. Lägg till lite rutor som organiserar och pilla även med 
en eventuell bakgrundsbild. Lägg till lite färg kanske?
-----------------------------------------------------------------------------------------------

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


from lap_timer import LapTimer
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from settings import Settings
from tracks import Tracks
from position import Position
from PIL import Image, ImageTk
import time
import json
import requests
from time import sleep
from os import sys
from gauges import Gauges
from rich.traceback import install
from rich.console import Console
#


class RaceWareDepot:
    
    def __init__(self):
        # Ett test av rich:s felhantering konsollmanipulering
        install()
        # Initerar en Console instans för att skriva ut finare meddelanden i terminalen.
        self.console = Console()
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
            'load' : 'ENGINE_LOAD',
            'fuel' : 'FUEL_LEVEL'
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
            'load' : {'unit' : 'hp', 'upper_limit' : None},
            'fuel' : {'unit' : '%', 'upper_limit' : None}
            }

        try: 
            self.obd_instance = OBDII()
            self.settings.obd_active = True
        # Ersätt med konkret fel.
        except Exception as e:
            self.console.print(e)
        else:
            # Update the command list.
            self.command_list = \
                self.obd_instance.get_available_commands(self.command_list)

        self._init_screen()
        #Testa anslutning till api.
        self._test_connection()

    def _test_connection(self):
        try:
            answer = self._send_data("/testconnection",)
        
            if answer['answer'] == "Ansluten":
                greeting_string = "Anslutning lyckad!"
                self.console.print("[bold green]"+ greeting_string + "\n" + "-"*len(greeting_string))
                self.connected = True
                messagebox.showinfo("Anslutning", "Ansluten till API")
                sleep(0.5) # För att låta fönstret skapas i operativsystemet
            else:
                fail_string = "Fel svar från API"
                self.console.print("[bold red]"+ fail_string + "\n" + "-"*len(fail_string))
                self.connected = False
                messagebox.showinfo("Anslutning", "Ej ansluten till API")
                sleep(0.5) # För att låta fönstret skapas i operativsystemet
        except Exception as e:
                fail_string = "Anslutning misslyckad."
                self.console.print("[bold red]"+ fail_string + "\n" + "-"*len(fail_string) + 
                    "\n Fel: ", e)
                self.connected = False
                messagebox.showinfo("Anslutning", f"Ej ansluten till API\n Felkod: {e}")
                sleep(0.5) # För att låta fönstret skapas i operativsystemet


    def _init_screen(self):

        self.root = tk.Tk()
        # Lägger till meny högst upp precis som alla program har.
        # Tanken är att denna ska kunna användas för diverse inställningar och kommandon.
        self._init_menu()
        self.root.attributes('-fullscreen', self.settings.fullscreen)
        # Sätt fönstrets ikon, har för mig att man måste spara som klassattribut.
        self.icon_photo = tk.PhotoImage(file = self.settings.script_path + "/images/storströg.png")
        self.root.iconphoto(False, self.icon_photo)
        if self.settings.fullscreen:
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


    def _init_menu(self):
        '''Ställer in menylisten högst upp'''
        # Ger ett mer professionellt intryck.
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu = self.menu_bar)
        file_menu = tk.Menu(self.menu_bar)
        settings_menu = tk.Menu(self.menu_bar)
        save_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label = 'Fil', menu = file_menu)
        file_menu.add_cascade(label = 'Spara', menu = save_menu)
        self.menu_bar.add_cascade(label = 'Inställningar', menu = settings_menu)
        # Flytta detta till en metod som skapar ett fönster där man får ange önskat värde.
        # Denna metod kan lämpligen ligga i settings.
        settings_menu.add_command(label = 'Uppdateringstid', command = lambda x = 'delay_time', 
            t = 10: self.settings.set(x, self.canvas, unit = "ms", label = 'Uppdateringstid'))
        settings_menu.add_command(label = 'Återanslut', command = lambda: self._test_connection())
        # .quit hade vart samma som lambda: sys.exit()
        file_menu.add_command(label = 'Avsluta', command = lambda: sys.exit())
        # För att spara JSON - filen.
        save_menu.add_command(label = 'Spara JSON...', command = lambda x = 'json': self.lap_timer.save_data(x)) #lambda: self._save_data('JSON')
        save_menu.add_command(label = 'Spara grafer...', command = lambda x = 'graph': self.lap_timer.save_data(x)) #lambda: self._save_data('Graph')
        save_menu.add_command(label = 'Spara båda...', command = None) #lambda: self._save_data('Both')

    # Funktion som löper kontinuerligt. Den har en tid efter vilken den kör.
    # I inställningar kan man modifiera denna tid.
    
    def _check_state(self):
        if self.settings.track_available and self.in_car:
            self._update_pos()
        self._update_values()
        self._update_screen()
        self.root.after(self.settings.delay_time,self._check_state)

    def _update_screen(self):
        if self.counting and self.connected:
            # Hämtar data från enheten i bilen.
            temp_dict = self._get_data('measurements')

            for key, value in temp_dict.items():
                self.gauge_dict[key].value = value

            for value in self.gauge_dict.values():
                value.give_gauge_value()
            
            print(self._get_data('gps_data'))

        # Räkna varvtid.
        try:
            if self.lap_timer.counter: 
             # Kolla här så att allt är ok.
             # Se till så att _format_time används i 
             # _update_pos()!
                self._update_pos()
        except AttributeError:
            pass 


    def _format_time(self):
        '''Formatterar ett antal sekunder'''
        # Här får jag fixa så att det blir fint.
        display_time = time.time() - self.lap_timer.start_time
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
        if self.lap_timer.counter:
            self.lap_timer.lap_time_label.config(text = self._format_time())

    def _toggle_measurements(self):
        self.lap_timer.start_count(self)
        if self.counting:
                self.counting = False
        else:
            self.counting = True

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

    def _send_data(self, resource, data = None):
        '''Metod som lagrar data i databas på FLASK REST-API'''
        # Kopierar mätarnas värden och lägger i ett dictionary som sedan
        # skickas med id data1.
        response = requests.get(self.settings.base_url + resource, data)

        return response.json()


    def _get_data(self, measurement):
        '''
        Metod som hämtar data från APIn. Measurement - argumentet anger vilken data man vill hämta.
        Man har 'measurements' och 'gps_data' som alternativ.
        '''
        if measurement == 'measurements':
            response = requests.get(self.settings.base_url + "measurements/data1")
            response = response.json()
            # Skickar ut data utan id.
            del response["id"]
            return response
        elif measurement == 'gps_data':
            return requests.get(self.settings.base_url + "location/gps").json()


    def run(self):
        self._update_screen()
        self.root.mainloop()

    def _init_track(self, track):
        '''
        Denna metod initerar skärmen som är igång när man är ute och kör.
        Alla mätare initeras tillsammans med GPS - positioneringen.
        '''
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
                highlightthickness = 0) 
            self.image_canvas.place(
                relx = self.settings.image_canvas_x,
                rely = self.settings.image_canvas_y,
                anchor = 'center',
                )
            self.image_canvas.create_image(
                0,
                0,
                anchor = 'nw', 
                image = self.track_image)
            # Lägg ut position på kartan.
            self.gps_pos = Position(self, self.canvas)
            # Väljer kartans canvas för att rita ut bilden.
            self.gps_pos.draw_pointer(self.image_canvas)
            # Flyttar ut punkten till mitten på banan.
            self.gps_pos.move(0.5, 0.5)
            self.lap_timer = LapTimer(self, self.canvas)
            self.lap_timer.draw_clock(0.45, 0.3, 'nw')
            self.settings.track_available = True
        else:
            # Det finns ingen bild, skriv ut ett meddelande på skärmen.
            self.no_picture_label = tk.Label(self.canvas, 
                text = self.settings.no_image_text, font=(self.settings.gauge_font,
				self.settings.gauge_font_size,),
                bg = self.canvas['background'],
                fg = 'white')
            self.no_picture_label.place(x = self.settings.screen_width * 0.75,
                y=self.settings.screen_height * 0.75,
                anchor = 'center',)
        


        # Fixa countknappen, det gör jag hellre här än i positionklassen

        self.start_count_button = tk.Button(self.canvas, text = "Start", 
            fg = self.settings.green_color, 
            command = lambda:  self._toggle_measurements())
        # rely = 0.15 linjerar i överkant med shiftlighten.
        self.start_count_button.place(relx = 0.9, rely = 0.15, anchor = 'ne')

        # Fixa mätare.
        self._init_gauges()
        # Visa varv data:
        self.lap_timer.init_lap_data(self)
        self._check_state()

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
            # If key not among the avaliable commands, skip.
            if not key in self.command_list.keys():
                continue
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
                if row == 4:
                    row = 1
                    column += 1    
                self.gauge_dict[key].show_gauge(type = 'grid', row = row, column = column)
                row += 1


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
    race = RaceWareDepot()
    race.run()

