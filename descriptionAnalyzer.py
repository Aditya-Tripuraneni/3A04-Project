from agents import Agent
from data import Data
from descriptionFinder import DescriptionFinder
from description import Description


class DescriptionAnalyzer(Agent):

    def __init__(self):
        self.prediction = None

    def analyze_data(self, data: Data):
        description_finder = DescriptionFinder(data)
        song_data = description_finder.identify_song()
        self.prediction = song_data.get_song_data()

    def get_confidence_score(self):
        return self.prediction["confidence_score"]
    
    def submit_partial_solution(self):
        return self.prediction


# Example usage
sample_description = Description(
    artist="Justin Timberlake",
    genre="Pop / R&B",
    year="2013",
    albumName="The 20/20 Experience",
    mood="Emotional, Romantic, Reflective",
    genderOfArtist="Male",
    language="English",
    region="North America",
    featuredArtist="None"
)


description_agent = DescriptionAnalyzer()
description_agent.analyze_data(sample_description)
    