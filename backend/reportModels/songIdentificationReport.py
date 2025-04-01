from report import Report

class SongIdentificationReport(Report):
    def __init__(self, songName, userGuess, songIdentified, accuracyScore, recommendedArtists, timestamp=None):
        super().__init__(songName, userGuess, songIdentified, accuracyScore, recommendedArtists, timestamp)
        

    def to_dict(self):
        return {
            "songName": self.songName,
            "userGuess": self.userGuess,
            "songIdentified": self.songIdentified,
            "accuracyScore": self.accuracyScore,
            "recommendedArtists": self.recommendedArtists,
            "timestamp": self.timestamp
        }