from agents import Agent
from audio import Audio
from audioAPI import AudioIdentifier
from data import Data


class AudioAnalyzer(Agent):

    def __init__(self):
        super().__init__()

    def analyze_data(self, data: Data):
        audio_finder = AudioIdentifier(data)

        song_data = audio_finder.identify_song()

        self.prediction = song_data.get_song_data()
        self.analyzed = True




# Example usage
sample_audio = Audio("ABC.mp3")
audio_analyzer = AudioAnalyzer()

audio_analyzer.analyze_data(sample_audio)
res = audio_analyzer.submit_partial_solution()
print(res)
print(audio_analyzer.get_confidence_score())

    

