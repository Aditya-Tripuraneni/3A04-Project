from abc import ABC, abstractmethod
from data import Data

class SongIdentifier:
    @abstractmethod
    def identify_song(data: Data):
        pass

