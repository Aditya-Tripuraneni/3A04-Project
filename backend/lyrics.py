from data import Data


class Lyrics(Data):
    """Represents lyrics data and provides access to it.

    This class stores lyrics information and allows retrieval 
    through a public method. Inherits from the Data class.
    """

    def __init__(self, lyrics: str):
        """Initializes a Lyrics object.

        Args:
            lyrics (str): The lyrics to be stored.
        """
        self.lyrics = lyrics
        self.data = {}
        self._store_data()

    def _store_data(self):
        """Stores the lyrics data internally.

        This is a protected method that sets the lyrics data
        in the internal dictionary. It is not intended to be 
        accessed directly outside the class.
        """
        self.data["lyrics"] = self.lyrics

    def get_lyrics_data(self) -> str:
        """Retrieves the stored lyrics.

        Returns:
            str: The lyrics stored in the object.
        """
        return self.data["lyrics"]
