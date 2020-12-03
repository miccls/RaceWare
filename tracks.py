# Initially I will add information manually but eventually 
# I might make it possible to just add a text file with 
# information of the tracks.
import tkinter as tk
from PIL import Image, ImageTk

class Tracks:
	''' A class to manage various tracks that we will visit '''
	def __init__(self, main):
		self.settings = main.settings
		'''Making dictionary containing track
		specific info'''
		self.tracks_dict = { 
			'mantorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'knutstorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'anderstorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'sturup' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123,},
			'ingen bana' : {'längd' : 0, 
			'longitud' : 0, 'latitud' : 0}
			}
		self.image_dict = {
			'sturup' : self.settings.script_path + '/track_images/sturup.png',
			'knutstorp' : self.settings.script_path + '/track_images/knutstorp.png'
			}

		self.settings = main.settings

	def get_image(self, track):

		# Kod här för att få till en schysst size på bilden.
		image_path = self.image_dict[track]
		im = Image.open(image_path)
		im_width = im.width
		desired_width = (self.settings.screen_width * 
			self.settings.map_scale)
		# Skalar om bilden så att dess bredd är en fjärdedel av skärmen
		resize_factor = desired_width / im_width
		im = im.resize((round(im.size[0]*resize_factor), round(im.size[1]*resize_factor)))
		im.save(self.settings.script_path + '/track_images/resized.png')
		return tk.PhotoImage(file = self.settings.script_path + '/track_images/resized.png')

