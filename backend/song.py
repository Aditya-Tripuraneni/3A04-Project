from .data import Data


class Song(Data):
    """Represents song data and provides access to it.

    This class stores song-related information, including the song name, 
    author, and a confidence score. It allows retrieval of this data 
    in a controlled manner to prevent direct modification.
    """

    def __init__(self, song_name: str, song_author: str, confidence_score: float):
        """Initializes a Song object.

        Args:
            song_name (str): The name of the song.
            song_author (str): The author or artist of the song.
            confidence_score (float): The confidence score of the song identification.
        
        This method sets up the song attributes and stores them in a dictionary.
        """
        self.song_name = song_name
        self.song_author = song_author
        self.confidence_score = confidence_score
        self.data = {}
        self._store_data()


    def _store_data(self):
        """Stores the song data internally.

        This is a protected method that sets the song data in the internal 
        dictionary. It is not intended to be accessed directly outside the class.
        """
        self.data = {
            "song_name": self.song_name,
            "song_author": self.song_author,
            "confidence_score": self.confidence_score
        }
        

    def get_song_data(self) -> dict:
        """Returns a copy of the song data.

        Returns:
            dict: A copy of the song data including song name, author, 
            and confidence score.

        Returns a copy instead of the original to prevent external modification.
        """
        return self.data.copy()
