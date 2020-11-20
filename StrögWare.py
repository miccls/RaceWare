'''
To do:

Fixa shiftlight.
7 lampor som räknar upp grönt och sedan blinka rött eller något.
Gör en grå rektangel vars storlek räknas fram av programmet 
Fyll den med 7 lamport var storlek är tidigare bestämd.
Ge lamporna en basfärg om lite ljusare grå för att sedan går till
rött och grönt. Kanske ge dem en lite större cirkel som är en annan
grå som bakgrund oc
'''


# Store gauge value in class and update it when reading new value.



import pygame
import sys
from time import sleep

from tracks import Tracks
from settings import Settings
from button import Button
from gauges import Gauges
from shiftlight import Shiftlight

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

		# Make all the sprite groups in the program
		self.track_buttons = pygame.sprite.Group()
		self.all_gauges = pygame.sprite.Group()


		self.screen = pygame.display.set_mode(
			(0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height

		# Make buttons to chose track.

		self._make_track_buttons()
		

	def _init_strögware(self):
		'''Setting the program up after the chosen track'''
		self.settings.strögware_active = True
		self.track_buttons.empty()
		del self.title
		pygame.mouse.set_visible(False)
		self._init_track(self.chosen_track)
		self._init_gauges()
		# Make instance of shiflight class.
		self.shiftlight = Shiftlight(self)


	def _init_track(self,track_choice):
		'''Help method to set everyting 
		up after the chosen track'''
		self.chosen_track_dict = self.tracks.tracks_dict[self.chosen_track]

		try:
			self.track_image = self.tracks.get_image(self.chosen_track.lower())
			self.track_image_rect = self.track_image.get_rect()
			current_ratio =self.track_image_rect.width / self.screen.get_rect().width
			# Scaling the picture to be a certain size.
			factor = self.settings.track_ratio/current_ratio
			self.track_image = pygame.transform.rotozoom(self.track_image, 0, factor)
			# Get new rect after rescaling and position at desireable place
			self.track_image_rect = self.track_image.get_rect()
			self.track_image_rect.bottomright = self.screen.get_rect().bottomright
			self.track_image_rect.x -= (self.track_image_rect.width) // 5
			self.track_image_rect.y -= (self.track_image_rect.height) // 5
			self.settings.track_available = True
		except:
			pass


	def _make_title(self, msg, font= 48):
		'''Make the title text displayed at the top'''
		title_text = msg
		self.title = Button(self,title_text, color = (0, 0, 0), font_size = font)
		self.title.rect.midtop = self.screen.get_rect().midtop
		self.title.image_rect.midtop = self.screen.get_rect().midtop
		self.title.rect.y += self.title.rect.height
		self.title.image_rect.y +=self.title.rect.height

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

	def _toggle(self,boolean):
		if boolean:
			return False
		else:
			return True
		print(boolean)

	def _check_keydown_events(self, event):
		# Code checking what buttons were pressed.
		if event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_c:
			self.settings.counter = self._toggle(self.settings.counter)

		
	def _check_buttons(self,mouse_pos):
		'''Kollar om någon av knapparna klickats på'''
		collision = False
		self.chosen_track = ''
		for sprite in self.track_buttons.sprites():
			if sprite.rect.collidepoint(mouse_pos):
				collision = True
				self.chosen_track = sprite.text

		if collision:
			self._init_strögware()


	def _init_gauges(self):
		'''Initiate the gauges'''
		gauge_title_color = (0xff,0xff,0xff)
		self.rpm_gauge = Gauges(self,'rpm:', font_size = 100)
		self.kph_gauge = Gauges(self,'km/h:', font_size = 100)
		#self.rpm_title_font = pygame.font.SysFont(None, 48)
		#self.kph_title_font = pygame.font.SysFont(None, 48)
		#self.rpm_title = self.rpm_title_font.render('RPM',
		#	True, gauge_title_color, self.settings.bg_color)
		#self.kph_title = self.rpm_title_font.render('KM/H',
		#	True, gauge_title_color, self.settings.bg_color)
		# Set the rects


		# Try to incorpoate the titles in the gauge class.
		# So that their rect and images are attributes of the gauge instance.

		self.rpm_gauge.label_image_rect.midleft = (
			self.screen.get_rect().midleft)
		self.kph_gauge.label_image_rect.midleft = (
			self.screen.get_rect().midleft)

		# Trying to express all rects relative to the screen rect
		# so that placements will adapt to different screens

		self.rpm_gauge.label_image_rect.x += self.settings.screen_width/10
		self.kph_gauge.label_image_rect.x += self.settings.screen_width/10

		self.rpm_gauge.label_image_rect.y -= self.settings.screen_height/6
		self.kph_gauge.label_image_rect.y += self.settings.screen_height/6

		self.rpm_gauge.gauge_rect.midleft = self.rpm_gauge.label_image_rect.midright
		self.kph_gauge.gauge_rect.midleft = self.kph_gauge.label_image_rect.midright

		self.rpm_gauge.default_rect = self.rpm_gauge.gauge_rect
		self.kph_gauge.default_rect = self.kph_gauge.gauge_rect


		# The -30 is to put distance 
		self.rpm_gauge.label_image_rect.midright = (
			self.rpm_gauge.gauge_rect.midleft)
		self.kph_gauge.label_image_rect.midright = (
			self.kph_gauge.gauge_rect.midleft)

		self.rpm_gauge.label_image_rect.x += self.settings.space
		self.kph_gauge.label_image_rect.x += self.settings.space

		#Add gauges to sprite group
		self.all_gauges.add(self.rpm_gauge)
		self.all_gauges.add(self.kph_gauge)


	def _update_gauge(self,gauge):
		# Fixa så att alla gauges uppdateras med deras värden
		gauge.give_gauge_value()
		gauge.gauge_rect.midleft = gauge.label_image_rect.midright
		


	def _update_screen(self):
		'''Update the screen'''

		self.screen.fill(self.settings.bg_color)
		if not self.settings.strögware_active:
			for sprite in self.track_buttons.sprites():
				sprite.draw_button()
			self.title.draw_button()

		if self.settings.counter:
			self.rpm_gauge.value += 50
			self.kph_gauge.value += 1
			if self.rpm_gauge.value > 8500:
				self.rpm_gauge.value = 0
				self.kph_gauge.value = 0
			sleep(0.05)

		if self.settings.strögware_active:
			for gauge in self.all_gauges.sprites():
				self._update_gauge(gauge)
				gauge.show_gauge()

			if self.settings.track_available:
				self.screen.blit(self.track_image, self.track_image_rect)

			self.shiftlight.update_colors(
				self.rpm_gauge.value)
			self.shiftlight.draw_shiftlight()

		pygame.display.flip()


	def run(self):
		while True:
			self._check_events()
			self._update_screen()


if __name__ == '__main__':
	strg = StrögWare()
	strg.run()