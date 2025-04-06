from .agents import Agent
from .lyricalFinder import LyricalFinder
from .data import Data
from .song import Song


class LyricalAnalyzer(Agent):
    """Analyzes lyrical data and predicts the song.

    This class processes lyrical data using the LyricalFinder agent
    to identify the song and extract useful metadata, such as 
    confidence scores and partial solutions.
    """

    def __init__(self):
        super().__init__()
    
    
    def analyze_data(self, data: Data) -> Song:
        """Analyzes the provided data and predicts the song.
        
         Args:
             data (Data): The lyrical data used to identify the song.
        
         This method creates a LyricalFinder instance, processes the input
         data, and stores the resulting song data in self.prediction.
        """
        lyrical_finder = LyricalFinder(data)
        song_data = lyrical_finder.identify_song()

        try:
            # Store the identified song data
            self.prediction = song_data.get_song_data()
            self.analyzed = True
            return song_data
        except:
            raise TypeError("Prediction only accepts type dict.")

    
   
