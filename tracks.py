# Initially I will add information manually but eventually 
# I might make it possible to just add a text file with 
# information of the tracks.
import pygame

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
			'sturup' : 'track_images/sturup.png',
			'knutstorp' : 'track_images/knutstorp.png'
			}

	def get_image(self, track):
		image_path = self.image_dict[track]
		return pygame.image.load(image_path)

