# Vad hände senast: Håller på att fixa knapparna. Dock, börja med att fixa
# run() så att skärmen går igång och fixa en _check_events() för att se till att
# skärmen stängs.



import pygame

from tracks import Tracks
from settings import Settings
from button import Button

class StrögWare:
	'''Main class of StrögWare. Contains high level logic
	managing all parts of the program'''

	def __init__(self):
		# Initiate the screen and all attributes of the instance.
		pygame.init()
		self.settings = Settings()
		# Screen initiated in fullscreen, 
		# Fitting for our system.

		# Making a Tracks instance to get all track info.
		self.tracks = Tracks()

		# Make a dictionary for all buttons.
		self.track_buttons = {}

		self.screen = pygame.display.set_mode(
			(0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height

		# Chose track.

		self._init_track()
		

	def _init_track(self):
		'''Help method to set everyting 
		up after the chosen track'''
		self._make_track_buttons()

	def _make_track_buttons(self):
		'''Makes the buttons for track choice'''
		i = 0
		self.key_list = []

		for key, value in self.tracks.tracks_dict.items():
			self.key_list.append(key)
			self.track_buttons[key] = Button(self,key)

		button_height = self.track_buttons[self.key_list[0]].rect.height

		# Moving the buttons out on the screen.
		for key in self.key_list:
			(self.track_buttons[key].rect.y + ((-1)^i)*i*
				button_height)
			(self.track_buttons[key].image_rect.y + ((-1)^i)*i*
				button_height)
			self.track_buttons[key].draw_button()

			i += 1

	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

	def _check_keydown_events(self, event):
		# Code checking what buttons were pressed.
		if event.key == pygame.K_q:
			sys.exit()
		

	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		for key in self.key_list:
			self.track_buttons[key].draw_button()

		pygame.display.flip()


	def run(self):
		while True:
			self._check_events()
			self._update_screen()
			# Before testing, make sure you can close the screen.
if __name__ == '__main__':
	strg = StrögWare()
	strg.run()