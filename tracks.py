# Initially I will add information manually but eventually 
# I might make it possible to just add a text file with 
# information of the tracks.


class Tracks:
	''' A class to manage various tracks that we will visit '''
	def __init__(self):
		self.tracks_dict = { 
			'mantorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'knutstorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'anderstorp' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'sturup' : { 'längd' : 1234, 
			'longitud' : 123, 'latitud' : 123},
			'ingen bana' : {'längd' : 0, 
			'longitud' : 0, 'latitud' : 0}
			}


