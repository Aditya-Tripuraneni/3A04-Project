from abc import ABC, abstractmethod
from typing import List
from song import Song
from models import SongPredictionResponse

class SongRecommender(ABC):
    """
    Interface for recommending songs based on an identified song.
    """
    
    def __init__(self, song_data: SongPredictionResponse):
        """
        Initialize the recommender with the identified song data.
        
        Args:
            song_data (SongPredictionResponse): The song data returned by the API
        """
        self.song_data = song_data
    
    @abstractmethod
    def recommend_songs(self) -> List[Song]:
        """
        Recommends songs based on the identified song.
        
        Returns:
            List[Song]: A list of recommended songs
        """
        pass 