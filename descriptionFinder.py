from description import Description
from songIdentifier import SongIdentifier
from model import multiturn_generate_content
from song import Song
from data import Data
import json
from jsonpath_ng import parse

class DescriptionFinder(SongIdentifier):
    def __init__(self, data: Description):
        self.description_data = data

    def __convert_to_string(self, data: dict) -> str:
        result = []
        for key, value in data.items():
            result.append(f"{key}: {value}")
        return "\n".join(result)

    def identify_song(self) -> Data:
        description = self.description_data.get_description_data()
        descriptionString = self.__convert_to_string(description)
        
        # prompt for the model to identify song based on description
        prompt = """Can you identify the song based on this description? 
                   Output the data in the form: "Name: Song Name Artist: Artist Name" Do this on the same line.
                   """
        
        query = prompt + "\n" + descriptionString

        # get results of the song and artist
        data = multiturn_generate_content(query)
        data = data.to_dict()

        # extract the song data in type DatumInContext 
        song_output = parse('candidates[0].content.parts[0].text').find(data)

        # extract the confidence value in type DatumInContext 
        avg_log_probability = parse('candidates[0].avg_logprobs').find(data)

        # extract the song name and the artist name from DatumInContext 
        song_info = song_output[0].value 

        # extract the confidence value from DatumInContext 
        confidence_score = avg_log_probability[0].value if avg_log_probability else None

        # Form of the song_info is "Name: XXX Artist: YYY"
        name_part, artist_part = song_info.split(' Artist:')

        song_name = name_part.replace("Name:", "").strip()
        artist_name = artist_part.strip()

        print(song_name)
        print(artist_name)

        song_data = Song(song_name, artist_name, confidence_score)

        return song_data 