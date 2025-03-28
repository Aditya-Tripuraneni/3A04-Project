from .agents import Agent
from .audioAPI import AudioIdentifier
from .data import Data
from .song import Song


class AudioAnalyzer(Agent):

    def __init__(self):
        super().__init__()

    def analyze_data(self, data: Data) -> Song:
        audio_finder = AudioIdentifier(data)

        song_data = audio_finder.identify_song()

        # store the identified song data
        try:
            self.prediction = song_data.get_song_data()
            self.analyzed = True
            return song_data
        except:
            raise TypeError("Prediction only accepts type dict.")






