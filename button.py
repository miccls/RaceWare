# Knapp - klass.

import pygame.font
from pygame.sprite import Sprite


class Button(Sprite):

	def __init__(self, main, msg, color = (30, 30, 30), font_size = 48):
		'''Hämtar nödvändig info för att göra en knapp'''

		super().__init__()

		self.screen = main.screen
		self.screen_rect = main.screen.get_rect()

		# Storlek på knappen.
		self.text = msg
		self.color = color
		self.text_color = (0xff, 0xff, 0xff)
		self.font = pygame.font.SysFont(None, font_size)

		# Intressant metod används här nedan för att skriva ut meddelandet på knappen

		self._prep_msg(msg)

		self.width, self.height = (self.image_rect.width * 1.2), (self.image_rect.height * 1.4)

		# Placera rect på rätt ställe på skärmen.

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center


	def _prep_msg(self, msg):
		''' Gör en bild av den test vi vill skriva ut i knappen '''
		self.msg_image = self.font.render(msg.title(), True, self.text_color, self.color)
		self.image_rect = self.msg_image.get_rect()
		self.image_rect.center = self.screen_rect.center

	def draw_button(self):
		''' Ritar ut knappen på skärmen '''
		self.screen.fill(self.color, self.rect)
		self.screen.blit(self.msg_image, self.image_rect)