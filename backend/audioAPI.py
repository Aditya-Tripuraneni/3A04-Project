from audio import Audio
from data import Data
from audioModel import classify_song
from song import Song
from songIdentifier import SongIdentifier 


class AudioIdentifier(SongIdentifier):
    def __init__(self, data: Audio):
        self.audio_data = data
    

    def identify_song(self) -> Data: 
        audio_file_path = self.audio_data.get_audio_data()

        # use model to identify song based on audio file
        song_data = classify_song(audio_file_path)

        # song result is in the form "Name: XXX Artist: YYY" Confidence: "Confidence"
        # extract the name, artist and confidence score
        song_info = song_data.split(' Confidence:')
        name_part, artist_part = song_info[0].split(' Artist:')
        song_name = name_part.replace("Name:", "").strip()
        artist_name = artist_part.strip()
        confidence_score = float(song_info[1].strip())

        song_data = Song(song_name, artist_name, confidence_score)

        return song_data

