
class Settings:
	'''Settings for the program'''
	def __init__(self):

		# These are defaults which get changed
		# in the main class with the FULLSCREEN command.
		self.screen_widht = 1920
		self.screen_height = 1080
		self.bg_color = (0, 0, 0)
		self.gauge_bg_color = (0,0,0)
		self.strögware_active = False
		self.space = -30 # Mimic the push of a spacebar in images
		self.counter = False
		self.track_available = False
		self.track_ratio = 0.4

		# For shiftlight
		self.light_number = 7
		self.space_between = 20
		self.light_radius = 50
		self.bg_heigth = 2.2*self.light_radius
		self.bg_width = (self.light_number*(2*self.light_radius + self.space_between) 
			+ 2*self.space_between)
		self.two_lights = 6000
		self.four_lights = 7000
		self.six_lights = 7500
		self.all_lights = 8000
