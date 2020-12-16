import os
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
class Settings:
	'''Settings for the program'''
	def __init__(self,in_car):

		# These are defaults which get changed
		# in the main class with the FULLSCREEN command.
		self.bg_color = '#000000' # FUTF-gul: #f1b434
		# Fixa filsökvägen där vi kör skriptet.
		self.script_path = os.path.dirname( os.path.abspath(__file__) )
		self.gauge_bg_color = (0,0,0)
		self.space = -30 # Mimic the push of a spacebar in images
		self.counter = False
		self.car_gauges = ['rpm', 'water', 'oiltemp']
		self.base_url = "http://192.168.1.129:5000/"

		# Applikationsspecifika inställningar
		if in_car:
			self.screen_width = 800   #800
			self.screen_height = 480  #480 är skärmen
			self.fullscreen = True
			self.delay_time = 20
			self.gauge_font_size = 24    
			self.timer_font_size = 40
			self.gauge_frame_width = 1
			self.gauge_frame_height = 0.5
			self.gauge_pos_x = 0.5
			self.gauge_pos_y = 0.75
			self.gauge_anchor = 'center'

		else:
			self.map_scale = 0.35
			# Relativa mått på var kartan ska placeras på skärmen.
			self.image_canvas_x = 0.75
			self.image_canvas_y = 0.65
			self.screen_width = 1920   #800
			self.screen_height = 1080 #480 är skärmen
			self.fullscreen = False
			self.delay_time = 500
			self.gauge_font_size = 36    
			self.timer_font_size = 54 
			self.gauge_frame_width = 0.35
			self.gauge_frame_height = 0.5
			self.gauge_pos_x = 0.05
			self.gauge_pos_y = 0.15
			self.gauge_anchor = 'nw'


		self.gauge_font = "System"
		self.timer_font = "System"
		self.no_image_text = "Karta saknas."
		self.pos_point_radius = 10
		self.button_color = 'white'
		# Ställer in refresh-tid.



		#GPS
		self.GPS_port = "/dev/ttyAMA0"

		# Flags, alla initeras som False
		self.track_available = False
		self.obd_active = False
		self.strögware_active = False


		# For shiftlight
		self.light_number = 9
		self.space_between = 20
		self.two_lights = 6000
		self.four_lights = 6500
		self.six_lights = 7000
		self.eight_lights = 7500
		self.all_lights = 8000
		self.green_color = '#09FF00'
		self.red_color = '#EC0202'
		self.gray_color = '#4F4F4F'
	
	def set(self, setting, master, unit = "", label = None):
		"""
		Sätter värdet på en önskad inställning
		"""
		# Skapar en dialogruta där man kan skriva in ett värde på önskad inställning
		if unit != "":
			unit = "[" + unit + "]"
		if not label:
			label = setting
		value = askstring(label, ('Ge värde: '+unit))
		setattr(self,setting, value)


