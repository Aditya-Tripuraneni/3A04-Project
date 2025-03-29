from .data import Data

class Audio(Data):
    def __init__(self, base64_audio: str):
        self.base64_audio = base64_audio

    def _store_data(self):
        pass

    def get_audio_data(self) -> str:
        return self.base64_audio
