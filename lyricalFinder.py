from lyrics import Lyrics
from songIdentifier import SongIdentifier
from model import multiturn_generate_content
from song import Song
from data import Data
from jsonpath_ng import parse


class LyricalFinder(SongIdentifier):
    """Identifies a song based on lyrical data.

    This class processes lyrics data using a language model to extract 
    song information, including the song name, artist, and confidence score.
    """

    def __init__(self, data: Lyrics):
        """Initializes a LyricalFinder object.

        Args:
            data (Lyrics): The lyrical data used for song identification.
        """
        self.lyrical_data = data

    
    def identify_song(self) -> Data:
        """Identifies the song based on the provided lyrics.

        Uses a language model to process the lyrics and extract 
        the song name, artist name, and confidence score.

        Returns:
            Data: A Song object containing the identified song data.
        """
        lyrics = self.lyrical_data.get_lyrics_data()

        # Construct the prompt for the model to identify the song.
        prompt = (
            "Can you identify the song? I will present the lyrics.\n"
            'Output the data in the form: "Name: Song Name Artist: Artist Name" '
            "on the same line."
        )
        
        query = prompt + "\n" + lyrics

        # Get the results from the language model.
        data = multiturn_generate_content(query)
        data = data.to_dict()

        # Extract the song output in the format:
        # candidates[0].content.parts[0].text -> "Name: XXX Artist: YYY"
        song_output = parse('candidates[0].content.parts[0].text').find(data)

        # Extract the confidence score (if available).
        avg_log_probability = parse('candidates[0].avg_logprobs').find(data)

        # Extract song information from the parsed result.
        song_info = song_output[0].value if song_output else None
        confidence_score = avg_log_probability[0].value if avg_log_probability else None

        if not song_info:
            raise ValueError("Failed to extract song information from model output.")

        # Split the result to extract song name and artist.
        name_part, artist_part = song_info.split(' Artist:')
        song_name = name_part.replace("Name:", "").strip()
        artist_name = artist_part.strip()

        print(song_name)
        print(artist_name)

        # Create a Song object containing the extracted data.
        song_data = Song(song_name, artist_name, confidence_score)

        return song_data
