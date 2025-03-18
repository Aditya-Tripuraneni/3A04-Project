from data import Data


class Song(Data):
    def __init__(self, song_name: str, song_author: str):
        self.song_name = song_name
        self.song_author = song_author
        self.data = None
        
    def store_data(self):
        self.data = {
            "song_name": self.song_name,
            "song_author": self.song_author
        }