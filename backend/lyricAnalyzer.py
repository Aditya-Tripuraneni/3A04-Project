from agents import Agent
from lyricalFinder import LyricalFinder
from data import Data
from song import Song


class LyricalAnalyzer(Agent):
    """Analyzes lyrical data and predicts the song.

    This class processes lyrical data using the LyricalFinder agent
    to identify the song and extract useful metadata, such as 
    confidence scores and partial solutions.
    """

    def __init__(self):
        super().__init__()
    
    
    def analyze_data(self, data: Data) -> Song:
        """Analyzes the provided data and predicts the song.
        
         Args:
             data (Data): The lyrical data used to identify the song.
        
         This method creates a LyricalFinder instance, processes the input
         data, and stores the resulting song data in self.prediction.
        """
        lyrical_finder = LyricalFinder(data)
        song_data = lyrical_finder.identify_song()
        
        # Store the identified song data
        self.set_prediction(song_data.get_song_data())

        self.analyzed = True

        return song_data

    
   

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

# lyric_data = Lyrics(stored_lyrics)

# lyrical_agent = LyricalAnalyzer()

# lyrical_agent.analyze_data(lyric_data)
# # print(f"Confidence Score: {lyrical_agent.get_confidence_score()}")
