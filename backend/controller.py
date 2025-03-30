from .audio import Audio
from .description import Description
from .blackboard import BlackBoard
from .blackboardkeys import FactKeys, PartialSolutionKeys
from .data import Data
from .lyricAnalyzer import LyricalAnalyzer
from .audioAnalyzer import AudioAnalyzer
from .descriptionAnalyzer import DescriptionAnalyzer
from .lyrics import Lyrics


class Controller:
    def __init__(self):
        self.blackboard = BlackBoard()
        self.lyrical_analyzer = LyricalAnalyzer()
        self.audio_analyzer = AudioAnalyzer()
        self.description_analyzer = DescriptionAnalyzer()

    
    def analyze_data(self, data: Data):
        """
        Analyzes the given data based on its type and stores relevant facts and partial solutions
        in the blackboard.
        
        Args:
            data (Data): The data to be analyzed. It can be of type Audio, Lyrics, or Description.
        """
        if isinstance(data, Audio):
            # Handle audio data
            song_prediction = self.audio_analyzer.analyze_data(data)
            audio_file = data.get_audio_data()
            self.blackboard.write_fact(FactKeys.AUDIO_FILE, audio_file)
            self.blackboard.write_partial_solution(PartialSolutionKeys.AUDIO_RESULT, song_prediction)

        elif isinstance(data, Lyrics):
            # Handle lyrics data
            song_prediction = self.lyrical_analyzer.analyze_data(data)
            lyrics = data.get_lyrics_data()
            self.blackboard.write_fact(FactKeys.LYRICAL_TEXT, lyrics)
            self.blackboard.write_partial_solution(PartialSolutionKeys.LYRICAL_RESULT, song_prediction)

        elif isinstance(data, Data):
            # Handle description data (generic Data type or specific subclass)
            song_prediction = self.description_analyzer.analyze_data(data)
            self.blackboard.write_fact(FactKeys.DESCRIPTION_TEXT, data)
            self.blackboard.write_partial_solution(PartialSolutionKeys.DESCRIPTION_RESULT, song_prediction)

        else:
            raise ValueError("Unsupported data type provided for analysis.")
    
    def finalize_solution(self):
        """
        Finalizes the solution by returning the song with the highest confidence score
        from the partial solutions stored in the blackboard.
        
        Returns:
            Song: The predicted song with the highest confidence score.
        """
        return self.blackboard.finalize_solution()
    
