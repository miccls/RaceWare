from settings import Settings
from tracks import Tracks
import tkinter as tk
from PIL import Image, ImageTk

class tkinterströg:

    def __init__(self):

        # Hämtar all tillgänglig ban-info.



        self.tracks = Tracks()

        # Använder Tkiner för att ställa in 
        # skärmen och startförhållanden.
        self._init_screen()


    def _init_screen(self):

        self.settings = Settings()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root,
            height = self.settings.screen_height,
            width = self.settings.screen_width,
            bg = self.settings.bg_color)
        self.canvas.pack()
        self.buttonframe = tk.Frame(self.canvas,
            bg = '#f5d742')
        self.buttonframe.place(relx = 0.5, rely = 0.5,
            anchor = 'center')
        self.button1 = tk.Button(self.buttonframe,
            bg = '#000000', highlightcolor = '#ffffff',
            text = 'Mantorp',
            width = 10,
            height = 2)
        button_dict = {}
        for key in self.tracks.tracks_dict.keys():
            button_dict[key] = tk.Button(self.buttonframe,
            bg = 'red', highlightcolor = 'red',
            text = key.title(),
            width = 15,
            height = 2,
            command = lambda track = key: self._init_track(track))   
            button_dict[key].pack()

    def run(self):
        self.root.mainloop()

    def _init_track(self,track):

        # När en bana blivit vald körs koden i denna metod.
        # Tar bort listan med knappar.
        self.buttonframe.destroy()
        self.track_dict = self.tracks.tracks_dict[track]
        self.track_image = self.tracks.get_image(track)
        image = self.canvas.create_image(600,600,anchor = 'center', image = self.track_image)
        


if __name__ == '__main__':
    strög = tkinterströg()
    strög.run()

