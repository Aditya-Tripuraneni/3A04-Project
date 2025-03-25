from agents import Agent
from audioAPI import AudioIdentifier
from data import Data
from song import Song


class AudioAnalyzer(Agent):

    def __init__(self):
        super().__init__()

    def analyze_data(self, data: Data) -> Song:
        audio_finder = AudioIdentifier(data)

        song_data = audio_finder.identify_song()

        # store the identified song data
        self.set_prediction(song_data.get_song_data())

        self.analyzed = True

        return song_data




# Example usage
# sample_audio = Audio("ABC.mp3")
# audio_analyzer = AudioAnalyzer()

# audio_analyzer.analyze_data(sample_audio)
# res = audio_analyzer.get_partial_solution()
# print(res)
# print(audio_analyzer.get_confidence_score())

    

