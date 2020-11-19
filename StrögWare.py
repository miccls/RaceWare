# Vad hände senast: Håller på att fixa knapparna. Dock, börja med att fixa
# run() så att skärmen går igång och fixa en _check_events() för att se till att
# skärmen stängs.



import pygame
import sys

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
		self.track_buttons = pygame.sprite.Group()

		self.screen = pygame.display.set_mode(
			(0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height

		# Make buttons to chose track.

		self._make_track_buttons()
		

	def _init_track(self,track_choice):
		'''Help method to set everyting 
		up after the chosen track'''
		if track_choice == 'ingen bana':
			track_choice = ''
		self._make_title(track_choice,font = 60)


	def _make_title(self, msg, font= 48):
		'''Make the title text displayed at the top'''
		title_text = msg
		self.title = Button(self,title_text, color = (0, 0, 0), font_size = font)
		self.title.rect.midtop = self.screen.get_rect().midtop
		self.title.image_rect.midtop = self.screen.get_rect().midtop
		self.title.rect.y += self.title.rect.height*2
		self.title.image_rect.y +=self.title.rect.height*2

	def _make_track_buttons(self):
		'''Makes the buttons for track choice'''

		# Make title screen image.
		self._make_title('välj bana:')

		i = 0
		shift_button = 0
		self.key_list = []

		for key, value in self.tracks.tracks_dict.items():
			self.key_list.append(key)
			new_button = Button(self,key)
			self.track_buttons.add(new_button)

		# Spacing between button on the screen
		for sprite in self.track_buttons.sprites():
			button_space = 2*sprite.rect.height
			break

		sign = 1
		# Moving the buttons out on the screen.
		for sprite in self.track_buttons.sprites():
			sign *= -1
			sprite.rect.y += (shift_button*
				button_space)*sign
			sprite.image_rect.y += (shift_button*
				button_space)*sign
			i += 1

			if (i+1)%2 == 0:
				shift_button += 1
			elif shift_button == 0:
				shift_button = 1


	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_buttons(mouse_pos)

	def _check_keydown_events(self, event):
		# Code checking what buttons were pressed.
		if event.key == pygame.K_q:
			sys.exit()
		
	def _check_buttons(self,mouse_pos):
		'''Kollar om någon av knapparna klickats på'''
		collision = False
		self.chosen_track = ''
		for sprite in self.track_buttons.sprites():
			if sprite.rect.collidepoint(mouse_pos):
				collision = True
				self.chosen_track = sprite.text

		if collision:
			self.settings.strögware_active = True
			self.track_buttons.empty()
			del self.title
			pygame.mouse.set_visible(False)
			print(self.chosen_track.title())
			self._init_track(self.chosen_track)




	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		if not self.settings.strögware_active:
			for sprite in self.track_buttons.sprites():
				sprite.draw_button()
		self.title.draw_button()

		pygame.display.flip()


	def run(self):
		while True:
			self._check_events()
			self._update_screen()
			# Before testing, make sure you can close the screen.
if __name__ == '__main__':
	strg = StrögWare()
	strg.run()