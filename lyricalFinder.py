from lyrics import Lyrics
from songIdentifier import SongIdentifier
from model import multiturn_generate_content
from song import Song
import json
from jsonpath_ng import parse


class LyricalFinder(SongIdentifier):
    def __init__(self, data: Lyrics):
        self.lyrical_data = data
    
    
    def identify_song(self):
        lyrics = self.lyrical_data.get_lyrics_data()
        
        # prompt for the model to identify song
        
        prompt = """Can you identify the song? I will present the lyrics. 
                    Output the data in the form: "Name: Song Name Artist: Artist Name" Do this on the same line. 
                  """
        
        query = prompt + "\n" + lyrics


        # get results of the song and artist
        data  = multiturn_generate_content(query)
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


        # string formatting to extract the song name and artist name

        name_part, artist_part = song_info.split(' Artist:')

        song_name = name_part.replace("Name:", "").strip()
        
        artist_name = artist_part.strip()

        print(song_name)
        print(artist_name)

        song_data = Song(song_name, artist_name)

        return song_data






stored_lyrics = """
Never know when someone come and try to take my life
I been sleepin' with the .45 like every night
In the whip, I pray to God I don't see flashin' lights
Goddamn they right behind me
And I wake up everyday, I wake up everyday with this anxiety
And they know where I stay
Got "Malone" on my plates
And they followin' me
Two hundred bands under the floor of the kitchen
A little more up in the walls and the ceilin'
Even family and friends started switchin'
Ever since I got that check, seen 'em itchin'
Eyes open, I see you, I'm watchin' you, yeah
More people wanna be you, don't trust no one
Tell me why I can't get no relief
Wonderin' when they'll come for me
A paranoid man makes paranoid plans
I'll do what I can, but it's out of my hands
Strugglin' just to find my peace
Sometimes feel like I got no friends
Can't trust a soul like I'm Snowden
Right by the bed, keep it loaded
Lord, have mercy if they broken
I don't ever sleep, yeah, I'm wide awake
If you try to pull up to my place
Beam is gonna hit you a mile away
I promise one of us gonna die today
Helicopters in the sky
No, he can't escape the eyes
Politicians and the lies
Tell me what's the point of pickin' sides
Tell me why I can't get no relief
Wonderin' when they'll come for me
A paranoid man makes paranoid plans
I'll do what I can, but it's out of my hands
Strugglin' just to find my peace
Mind is runnin' all day
Cost me more than money and I'm payin' the price, yeah
I ain't goin' nowhere
Killin' myself so I can make me a life, yeah
Minute after minute
Never had a limit
Woke up every mornin', knew that I just had to get it
Windows always tinted
You ain't lookin' in it
Either way I know they'll come for me again
Tell me why I can't get no relief
Wonderin' when they'll come for me
A paranoid man makes paranoid plans
I'll do what I can, but it's out of my hands
Strugglin' just to find my peace
"""

lyric_data = Lyrics(stored_lyrics)
lyrical_finder = LyricalFinder(lyric_data)

res = lyrical_finder.identify_song()
