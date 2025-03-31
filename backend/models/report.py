from abc import ABC, abstractmethod
from datetime import datetime

class Report(ABC):
    def __init__(self, songName, userGuess, songIdentified, accuracyScore, recommendedArtists, timestamp=None):
        self.songName = songName
        self.userGuess = userGuess
        self.songIdentified = songIdentified
        self.accuracyScore = accuracyScore
        self.recommendedArtists = recommendedArtists
        self.timestamp = timestamp or datetime.now().isoformat()

    @abstractmethod
    def to_dict(self):
        """Convert the report to a dictionary for saving to Firestore."""
        pass