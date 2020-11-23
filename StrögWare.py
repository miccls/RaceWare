'''
To do:

BOOM -> Byt GUI till Tkinter

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


# Store gauge value in class and update it when reading new value.



import pygame as pg
import tkinter as tk
import sys
from time import sleep

from tracks import Tracks
from settings import Settings
from button import Button
from gauges import Gauges
from shiftlight import Shiftlight
from obd_com import OBDII

class StrögWare:
	'''Main class of StrögWare. Contains high level logic
	managing all parts of the program'''

	def __init__(self):
		# Initiate the screen and all attributes of the instance.
		pg.init()
		self.settings = Settings()

		# List of commands available from OBDII
		self.command_list = {
    		'rpm' : 'RPM',
 			'kph' : 'SPEED',
      		'throttle' : 'THROTTLE_POS',
      		'water' : 'COOLANT_TEMP',
      		'oil' : 'OIL_TEMP',
      		'load' : 'ENGINE_LOAD'
      		}

		# Making a Tracks instance to get all track info.
		self.tracks = Tracks()

		# Make all the sprite groups in the program
		self.track_buttons = pg.sprite.Group()
		self.all_gauges = pg.sprite.Group()

		# Using the pygame FULLSCREEN feature to atomatically
		# fit the screen
		self.screen = pg.display.set_mode(
			(0, 0), pg.FULLSCREEN)
		# Passing the fitted size to settings instance
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height

		# Make buttons to chose track.

		self._make_track_buttons()
		

	def _init_strögware(self):
		'''Setting the program up after the chosen track'''
		# Active flag set to true
		self.settings.strögware_active = True
		# Remove the choice buttons.
		self.track_buttons.empty()
		# Remove choice text
		del self.title
		# Remove cursor for a cleaner look
		pg.mouse.set_visible(False)
		# Set 
		self._init_track(self.chosen_track)
		try:
			obd2 = OBDII(self)
		except:
			pass
		self._init_gauges()
		# Make instance of shiflight class.
		self.shiftlight = Shiftlight(self)


	def _init_track(self,track_choice):
		'''Help method to set everyting 
		up after the chosen track'''
		self.chosen_track_dict = self.tracks.tracks_dict[self.chosen_track]
		# The try-except block is used to avoid errors if a track doesn't have
		# an image to displat
		try:
			self.track_image = self.tracks.get_image(self.chosen_track.lower())
			self.track_image_rect = self.track_image.get_rect()
			current_ratio =self.track_image_rect.width / self.screen.get_rect().width
			# Scaling the picture to be a certain size.
			factor = self.settings.track_ratio/current_ratio
			self.track_image = pg.transform.rotozoom(self.track_image, 0, factor)
			# Get new rect after rescaling and position at desireable place
			self.track_image_rect = self.track_image.get_rect()
			self.track_image_rect.bottomright = self.screen.get_rect().bottomright
			self.track_image_rect.x -= (self.track_image_rect.width) // 5
			self.track_image_rect.y -= (self.track_image_rect.height) // 5
			self.settings.track_available = True
		except:
			pass
			# In place of pass, add code to display a 'Ingen bild tillgänglig' message.


	def _make_title(self, msg, font= 48):
		'''Make the title text displayed at the top'''
		title_text = msg
		# Using the functionality of the already written button class
		# in order to display the prompt 'Välj bana:' at the top of the screen
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

		# Adding choice buttons to a sprite group to be able to treat
		# them as one object
		for key, value in self.tracks.tracks_dict.items():
			self.key_list.append(key)
			new_button = Button(self,key)
			self.track_buttons.add(new_button)

		# Spacing between button on the screen
		for sprite in self.track_buttons.sprites():
			button_space = 2*sprite.rect.height
			break

		sign = 1
		# Spacing buttons on screen.
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
		''' Statemachine to check events and take
		appropriate action '''
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pg.MOUSEBUTTONDOWN:
				mouse_pos = pg.mouse.get_pos()
				self._check_buttons(mouse_pos)

	def _toggle(self,boolean):
		'''Used to toggle boolean value'''
		if boolean:
			return False
		else:
			return True
		print(boolean)

	def _check_keydown_events(self, event):
		'''Method including everything to do
		when a certain key is pressed'''
		# Code checking what buttons were pressed.
		if event.key == pg.K_q:
			sys.exit()
		elif event.key == pg.K_c:
			self.settings.counter = self._toggle(self.settings.counter)

		
	def _check_buttons(self,mouse_pos):
		'''Checks if any choice buttons were pressed'''
		collision = False
		self.chosen_track = ''
		for sprite in self.track_buttons.sprites():
			if sprite.rect.collidepoint(mouse_pos):
				collision = True
				# Set chosen track to the pressed sprite
				self.chosen_track = sprite.text

		if collision:
			self._init_strögware()


	def _init_gauges(self):
		'''Initiate the gauges'''

		# Making two instances for rpm and speed.
		'''Beroende på vad vi kan få ut från OBDII så 
		 Lägger man till dem med följande kod
		 self.oil_pressure_gauge = Gauges(self, 'Oljetryck', font_size = 100, unit = 'Pa')
		 self.oil_temp_gauge = Gauges(self, 'Oljetemp', font_size = 100, unit = '°')
		'''
		# Lägg in så att mätarna placeras ut på samma sätt som track buttons!

		self.rpm_gauge = Gauges(self,'rpm:', font_size = 100)
		self.kph_gauge = Gauges(self,'km/h:', font_size = 100)


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
		# Set background color to the one specified in settings instance
		self.screen.fill(self.settings.bg_color)
		# If program is still in initaial stage,
		# draw the buttons
		if not self.settings.strögware_active:
			for sprite in self.track_buttons.sprites():
				sprite.draw_button()
			self.title.draw_button()
		# De soft, denna används nu för att testa visarna.
		if self.settings.counter:
			self.rpm_gauge.value += 50
			self.kph_gauge.value += 1
			if self.rpm_gauge.value > 8500:
				self.rpm_gauge.value = 0
				self.kph_gauge.value = 0
			sleep(0.05)

		if self.settings.strögware_active:
			# Updating gauges with their respective values
			for gauge in self.all_gauges.sprites():
				self._update_gauge(gauge)
				gauge.show_gauge()

			if self.settings.track_available:
				# If the track is available, draw it on screen
				self.screen.blit(self.track_image, self.track_image_rect)
				# Här under lägger man in kod för att rita ut 
				# bilen på banan med avseende på GPS - värden.
			# Uppdatera shiftlighten med RPMvärdet
			self.shiftlight.update_colors(
				self.rpm_gauge.value)
			self.shiftlight.draw_shiftlight()
		# Show the updated screen.
		pg.display.flip()


	def run(self):
		while True:
			# Used to gather the big methods that handle
			# the general logic of the program
			self._check_events()
			self._update_screen()

# Only run the program if run from this file
if __name__ == '__main__':
	strg = StrögWare()
	strg.run()