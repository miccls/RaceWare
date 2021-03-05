
import tkinter as tk

class Shiftlight:
	'''Class that makes and handles the shiftligt'''
	def __init__(self,main,master):

		self.settings = main.settings

		# Make shiftlight frame
		self.canvas_width = self.settings.screen_width * 0.5
		self.canvas_height = self.settings.screen_height * 0.1
		self.bg_color = (30,30,30)
		self.shiftlight_canvas = tk.Canvas(master,
			width = self.canvas_width,
			height = self.canvas_height,
			bg = master['background'],
			highlightthickness=0)
		self.shiftlight_canvas.place(relx = 0.5, rely = 0.15, anchor = 'center')
		light_width = self.canvas_width / self.settings.light_number
		self.light_dict = {}
		for number in range(0, self.settings.light_number):
			self.light_dict[str(number + 1)] = self.shiftlight_canvas.create_rectangle(	
				light_width*number, self.canvas_height, 
				light_width*(number+1), 0, fill = self.settings.gray_color, 
				outline = self.settings.gray_color)
		

	def update_colors(self,rpm):
		'''Updates the color if the shiftlight.'''

		# Change this if desired, to potentially use 
		# self.light_number vaeiable to chose lights.
		if rpm > self.settings.two_lights and (
			rpm < self.settings.four_lights):
			level = 1
			color = self.settings.green_color
		elif rpm >= self.settings.four_lights and (
			rpm < self.settings.six_lights):
			level = 2
			color = self.settings.green_color
		elif rpm >= self.settings.six_lights and (
			rpm < self.settings.eight_lights):
			level = 3
			color = self.settings.green_color
		elif rpm >= self.settings.eight_lights and (
			rpm < self.settings.all_lights):
			level = 4
			color = self.settings.green_color
		elif rpm >= self.settings.all_lights:
			level = 5
			color = self.settings.red_color
		else:
			level = 0
		# Beroende på variablen level, ställ in färger.
		for number in range(1,self.settings.light_number+1):
				if number <= level or number > self.settings.light_number - level:
					self.shiftlight_canvas.itemconfig(self.light_dict[str(number)], fill = color)
				else:
					self.shiftlight_canvas.itemconfig(self.light_dict[str(number)], fill = self.settings.gray_color)