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

        # store the identified song data
        self.set_prediction(song_data.get_song_data())

    
        self.analyzed = True

        return song_data



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


# description_agent = DescriptionAnalyzer()
# description_agent.analyze_data(sample_description)
    