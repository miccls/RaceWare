import tkinter as tk

# Gå in i dokumentationen och kolla upp label och place()

class Gauges:
	''' To display text for gauges '''
	def __init__(self, master, label_text, main, unit = '', upper_limit = None):

		# Font and text settings
		self.upper_limit = upper_limit
		self.settings = main.settings
		self.master = master
		self.text_color = (0xff,0xff,0xff)
		self.value = 0
		# Prepare the image of the gauge - number.
		self.label_text = label_text
		self.tklabel = tk.Label(master, text = self.label_text,
			bg = master['background'],font=(self.settings.gauge_font,
			self.settings.gauge_font_size,),
			fg = 'white', height = 2)
		self.unit = ' ' + unit # Add space
		self.give_gauge_value()
		# Making gauge label and image.
		# This label is used to show what is being displayed
		
		
	def give_gauge_value(self):
		'''Make gauge value into image'''
		gauge_str = self.label_text.title() + ':' + (str(self.value) + self.unit)
		self.tklabel['text'] = gauge_str
		if self.upper_limit is not None:
			if self.value > self.upper_limit:
				self.tklabel['fg'] = self.settings.red_color
			else:
				self.tklabel['fg'] = 'white'

	def show_gauge(self):
		'''Draw the gauge on the screen'''
		self.tklabel.pack()

