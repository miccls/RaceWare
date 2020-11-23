
import pygame

class Shiftlight:
	'''Class that makes and handles the shiftligt'''
	def __init__(self,main):

		self.screen = main.screen
		self.screen_rect = self.screen.get_rect()

		self.settings = main.settings

		# Make shiftlight background

		self.bg_rect = pygame.Rect(0,0,self.settings.bg_width,self.settings.bg_heigth)
		self.bg_rect.midtop = self.screen_rect.midtop
		self.bg_rect.y += self.bg_rect.height//3
		self.bg_color = (30,30,30)

		# Light colors
		self.gray = (60, 60, 60)
		self.green = (0, 255, 0)
		self.red = (255, 0, 0)

		y_pos = self.bg_rect.y + self.settings.bg_heigth//2


		# Fixing the midpoints of all circles here.
		self.light_centers = {}
		for number in range(1,self.settings.light_number+1):
			x_pos = self.bg_rect.left + (number)*(self.settings.space_between +
				(self.settings.light_radius*2)) - self.settings.light_radius
			self.light_centers[str(number)] = (x_pos, y_pos)

		self.light_colors = {}
		for number in range(1,self.settings.light_number+1):
			self.light_colors[str(number)] = self.gray

	def update_colors(self,rpm):
		'''Set lights depending on rpm'''
		for number in range(1, self.settings.light_number+1):
				self.light_colors[str(number)] = self.gray

		# Change this if desired, to potentially use 
		# self.light_number vaeiable to chose lights.

		if rpm > self.settings.two_lights and (
			rpm < self.settings.four_lights):
			self.light_colors['1'] = self.green
			self.light_colors['7'] = self.green
		elif rpm >= self.settings.four_lights and (
			rpm < self.settings.six_lights):
			self.light_colors['1'] = self.green
			self.light_colors['7'] = self.green
			self.light_colors['2'] = self.green
			self.light_colors['6'] = self.green
		elif rpm >= self.settings.six_lights and (
			rpm < self.settings.all_lights):
			self.light_colors['1'] = self.green
			self.light_colors['7'] = self.green
			self.light_colors['2'] = self.green
			self.light_colors['6'] = self.green
			self.light_colors['3'] = self.green
			self.light_colors['5'] = self.green
		elif rpm >= self.settings.all_lights:
			for number in range(1,self.settings.light_number+1):
				self.light_colors[str(number)] = self.red

	def draw_shiftlight(self):
		''' Draw all the shiftlight '''
		pygame.draw.rect(
			self.screen, self.bg_color, self.bg_rect)
		for number in range(1, self.settings.light_number+1):
			light_number = str(number)
			pygame.draw.circle(self.screen, self.light_colors[light_number],
				self.light_centers[light_number], self.settings.light_radius)

	
