from data import Data


class Song(Data):
    def __init__(self, song_name: str, song_author: str, confidence_score: float):
        self.song_name = song_name
        self.song_author = song_author
        self.confidence_score = confidence_score
        self.data = {}
        self._store_data()
        
    def _store_data(self):
        self.data = {
            "song_name": self.song_name,
            "song_author": self.song_author,
            "confidence_score": self.confidence_score
        }

    def get_song_data(self):
        # copy so that original data can't be modified
        return self.data.copy()