from agents import Agent
from data import Data
from naturalLanguageProcessor import DescriptionFinder
from description import Description
from song import Song


class DescriptionAnalyzer(Agent):

    def __init__(self):
        super().__init__()
        

    def analyze_data(self, data: Data) -> Song:
        description_finder = DescriptionFinder(data)
        song_data = description_finder.identify_song()

        try:
            # store the identified song data
            self.prediction = song_data.get_song_data()
            self.analyzed = True
            return song_data
        except:
            raise TypeError("Prediction only accepts type dict.")




# Example usage


    