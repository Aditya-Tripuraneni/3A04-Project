from data import Data



class Lyrics(Data):
    def __init__(self, lyrics: str):
        self.lyrics = lyrics
        self.data = {}
        self._store_data()
    
    """
    Protected method, not meant to be called outside this class. 
    """
    def _store_data(self):
        self.data["lyrics"] = self.lyrics


    def get_lyrics_data(self):
        return self.data["lyrics"]
