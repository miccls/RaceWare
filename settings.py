import os

class Settings:
	'''Settings for the program'''
	def __init__(self):

		# These are defaults which get changed
		# in the main class with the FULLSCREEN command.
		self.screen_width = 800
		self.screen_height = 400
		self.bg_color = '#f1b434' # FUTF-gul: #f1b434
		# Fixa filsökvägen där vi kör skriptet.
		self.script_path = os.path.dirname( os.path.abspath(__file__) )
		self.gauge_bg_color = (0,0,0)
		self.space = -30 # Mimic the push of a spacebar in images
		self.counter = False
		self.map_scale = 0.35
		self.gauge_frame_width = 0.35
		self.gauge_frame_height = 0.65
		self.gauge_font_size = 12    #36 har jag använt från början
		self.gauge_font = "Helvetica"
		self.timer_font_size = 40  # 54
		self.timer_font = "Helvetica"
		self.no_image_text = "Karta saknas."
		self.pos_point_radius = 10
		self.button_color


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
