
from data import Data


class Audio(Data):
    def __init__(self, audio_file: str):
        self.audio_file = audio_file
    
    def _store_data():
        pass

    def get_audio_data(self) -> str:
        return  self.audio_file
