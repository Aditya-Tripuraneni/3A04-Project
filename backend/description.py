from .data import Data

class Description(Data):
    def __init__(
            self, 
            artist: str, 
            genre: str, 
            year: str, 
            albumName: str, 
            mood: str, 
            genderOfArtist: str, 
            language: str, 
            region: str, 
            featuredArtist: str
        ): 
        
        self.artist = artist
        self.genre = genre
        self.year = year
        self.albumName = albumName
        self.mood = mood
        self.genderOfArtist = genderOfArtist
        self.language = language
        self.region = region
        self.featuredArtist = featuredArtist
        self.data = {}
        self._store_data()
    
    """
    Protected method, not meant to be called outside this class. 
    Purpose is to store description attributes which make up a song.
    """
    def _store_data(self):
        self.data["artist"] = self.artist if self.artist else "Unknown"
        self.data["genre"] = self.genre if self.genre else "Unknown"
        self.data["year"] = self.year if self.year else "Unknown"
        self.data["albumName"] = self.albumName if self.albumName else "Unknown"
        self.data["mood"] = self.mood if self.mood else "Unknown"
        self.data["genderOfArtist"] = self.genderOfArtist if self.genderOfArtist else "Unknown"
        self.data["language"] = self.language if self.language else "Unknown"
        self.data["region"] = self.region if self.region else "Unknown"
        self.data["featuredArtist"] = self.featuredArtist if self.featuredArtist else "Unknown" 



    def get_description_data(self):
        return self.data.copy()
        
