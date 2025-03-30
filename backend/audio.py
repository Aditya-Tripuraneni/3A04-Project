from .data import Data

class Audio(Data):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _store_data(self):
        pass

    def get_audio_data(self) -> str:
        return self.file_path
