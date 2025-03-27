from audio import Audio
from description import Description
from blackboard import BlackBoard
from blackboardkeys import FactKeys, PartialSolutionKeys
from data import Data
from lyricAnalyzer import LyricalAnalyzer
from audioAnalyzer import AudioAnalyzer
from descriptionAnalyzer import DescriptionAnalyzer
from lyrics import Lyrics


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
    
   
    
    
stored_lyrics = """
The club isn't the best place to find a lover
So the bar is where I go
Me and my friends at the table doing shots
Drinking fast and then we talk slow
Come over and start up a conversation with just me
And trust me I'll give it a chance now
Take my hand, stop, put Van the Man on the jukebox
And then we start to dance, and now I'm singing like
Girl, you know I want your love
Your love was handmade for somebody like me
Come on now, follow my lead
I may be crazy, don't mind me
Say, boy, let's not talk too much
Grab on my waist and put that body on me
Come on now, follow my lead
Come, come on now, follow my lead
I'm in love with the shape of you
We push and pull like a magnet do
Although my heart is falling too
I'm in love with your body
And last night you were in my room
And now my bedsheets smell like you
Every day discovering something brand new
I'm in love with your body
(Oh-I-oh-I-oh-I-oh-I)
I'm in love with your body
(Oh-I-oh-I-oh-I-oh-I)
I'm in love with your body
(Oh-I-oh-I-oh-I-oh-I)
I'm in love with your body
Every day discovering something brand new
I'm in love with the shape of you
One week in we let the story begin
We're going out on our first date
You and me are thrifty, so go all you can eat
Fill up your bag and I fill up a plate
We talk for hours and hours about the sweet and the sour
And how your family is doing okay
And leave and get in a taxi, then kiss in the backseat
Tell the driver make the radio play, and I'm singing like
Girl, you know I want your love
Your love was handmade for somebody like me
Come on now, follow my lead
I may be crazy, don't mind me
Say, boy, let's not talk too much
Grab on my waist and put that body on me
Come on now, follow my lead
Come, come on now, follow my lead
I'm in love with the shape of you
We push and pull like a magnet do
Although my heart is falling too
I'm in love with your body
And last night you were in my room
And now my bedsheets smell like you
Every day discovering something brand new
"""

# was experiementing with the controller commented out for now


# controller = Controller()

# controller.analyze_data(Lyrics(stored_lyrics))

# res_ting = controller.finalize_solution()
# print(res_ting.get_song_data())

# # Example usage
# sample_description = Description(
#     artist="Justin Timberlake",
#     genre="Pop / R&B",
#     year="2013",
#     albumName="The 20/20 Experience",
#     mood="Emotional, Romantic, Reflective",
#     genderOfArtist="Male",
#     language="English",
#     region="North America",
#     featuredArtist="None"
# )

# controller.analyze_data(sample_description)
# res_2 = controller.finalize_solution()
# print(res_2.get_song_data())
