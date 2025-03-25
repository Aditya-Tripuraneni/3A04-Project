from abc import ABC, abstractmethod
from data import Data


class SongIdentifier(ABC):
    """Abstract base class for song identification.

    This class defines the interface for identifying songs 
    based on provided data. Subclasses must implement the 
    `identify_song` method.
    """

    @abstractmethod
    def identify_song(data: Data):
        """Identifies a song based on the input data.

        Args:
            data (Data): The data containing song-related information.

        Returns:
            Song: An instance of the identified song.

        This method must be implemented by any concrete subclass.
        """
        pass
