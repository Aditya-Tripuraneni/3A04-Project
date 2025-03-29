from .controller import Controller
from .description import Description
from .lyrics import Lyrics
from .audio import Audio
from .models import AnalyzeRequest, SongPredictionResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging 

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)



@app.post("/analyze_song")
async def analyze_song(request: AnalyzeRequest):
    """
    Analyzes the provided song data (lyrics, audio, description) and returns the predicted song,
    artist, and confidence score.
    """

    try:
        controller = Controller()

        if request.lyrics_request:
            lyrics = Lyrics(request.lyrics_request.lyrics)
            controller.analyze_data(lyrics)
            
        if request.description_request:
            description = Description(**request.description_request.model_dump())
            controller.analyze_data(description)

        if request.audio_request:
            print(f"Audio request received {request.audio_request.audio_file}")
            logger.debug(f"Audio file: {request.audio_request.audio_file}")
            audio = Audio(request.audio_request.audio_file)
            controller.analyze_data(audio)

        final_song = controller.finalize_solution()
        final_song_data = final_song.get_song_data()

        return SongPredictionResponse(**final_song_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

