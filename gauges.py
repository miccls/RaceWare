import pygame.font
from pygame.sprite import Sprite

class Gauges(Sprite):
	''' To display text for gauges '''
	def __init__(self,main, label,font_size = 48, unit = ''):

		super().__init__()

		self.screen = main.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = main.settings
		self.default_rect = 0
		# Font and text settings

		self.text_color = (0xff,0xff,0xff)
		self.font = pygame.font.SysFont(None,font_size)
		self.value = 0
		# Prepare the immage of the gauge - number.
		self.unit = ' ' + unit # Add space
		self.give_gauge_value()
		self.default_rect = self.gauge_rect


		# Making gauge label and image.
		# This label is used to show what is being displayed
		self.label_text = label
		self.label_image = self.font.render(label.upper(),
			True, self.text_color, self.settings.bg_color)
		self.label_image_rect = self.label_image.get_rect()

	def give_gauge_value(self):
		'''Make gauge value into image'''
		gauge_str = (str(self.value) + self.unit)
		self.gauge_image = self.font.render(gauge_str, True,
			self.text_color, self.settings.gauge_bg_color)
		# Placing the text in appropriate place
		self.gauge_rect = self.gauge_image.get_rect()

	def show_gauge(self):
		'''Draw the gauge on the screen'''
		self.screen.blit(self.label_image, self.label_image_rect)
		self.screen.blit(self.gauge_image, self.gauge_rect)

