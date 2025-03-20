from agents import Agent
from lyricalFinder import LyricalFinder
from data import Data
from lyrics import Lyrics

class LyricalAnalyzer(Agent):

    def analyze_data(self, data: Data):
        lyrical_finder = LyricalFinder(data)
        song_data = lyrical_finder.identify_song()
        print(song_data.get_song_data())

    def get_confidence_score(self):
        return 0.5
    
    def submit_partial_solution(self):
        return 6
    


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

lyrical_agent = LyricalAnalyzer()

lyrical_agent.analyze_data(lyric_data)