# Initially I will add information manually but eventually 
# I might make it possible to just add a text file with 
# information of the tracks.
import tkinter as tk
from PIL import Image, ImageTk

class Tracks:
	''' A class to manage various tracks that we will visit '''
	def __init__(self):
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
			'sturup' : '/Users/martinsvardsjo/Documents/Str-gWare/track_images/sturup.png',
			'knutstorp' : '/Users/martinsvardsjo/Documents/Str-gWare/track_images/knutstorp.png'
			}

	def get_image(self, track):

		# Kod här för att få till en schysst size på bilden.
		image_path = self.image_dict[track]
		im = Image.open(image_path)
		im = im.resize((round(im.size[0]*0.25), round(im.size[1]*0.25)))
		im.save('resized.png')
		return tk.PhotoImage(file = 'resized.png')

