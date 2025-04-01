from typing import List
from song import Song
from songRecommender import SongRecommender
from .textModel import multiturn_generate_content
from jsonpath_ng import parse

class ArtistBasedRecommender(SongRecommender):
    """
    Recommends songs based on the artist of the identified song.
    """
    
    def recommend_songs(self) -> List[Song]:
        """
        Recommends songs by the same artist as the identified song.
        
        Returns:
            List[Song]: A list of songs by the same artist
        """
        # Create a prompt for the model
        prompt = f"""Based on the song '{self.song_data.song_name}' by {self.song_data.song_author}, 
        recommend 5 other songs by the same artist ({self.song_data.song_author}). 
        For each song, output in the format: "Name: Song Name Artist: {self.song_data.song_author}"
        Put each song on a new line.
        """
        
        # Get recommendations from the model
        data = multiturn_generate_content(prompt)
        data = data.to_dict()

        # Extract the recommendations text
        recommendations_output = parse('candidates[0].content.parts[0].text').find(data)
        recommendations_text = recommendations_output[0].value

        # Split recommendations into individual songs
        song_lines = recommendations_text.strip().split('\n')
        songs = []
        
        for line in song_lines:
            if 'Name:' in line and 'Artist:' in line:
                name_part, artist_part = line.split(' Artist:')
                song_name = name_part.replace("Name:", "").strip()
                artist_name = artist_part.strip()
                
                song_data = Song(song_name, artist_name, 0.0)  # Using 0.0 for confidence score as it is irrelevant for this recommender
                songs.append(song_data)

        return songs 