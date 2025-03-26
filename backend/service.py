from audio import Audio
from controller import Controller
from description import Description
from lyrics import Lyrics
from models import LyricsRequest, DescriptionRequest, AudioRequest, SongPredictionResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    lyrics_request: LyricsRequest | None = None
    description_request: DescriptionRequest | None = None

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

        # if audio_request:
            #     audio = Audio(audio_request.audio_file)
            #     # analyze the audio data
            #     controller.analyze_data(audio)

        final_song = controller.finalize_solution()
        final_song_data = final_song.get_song_data()

        return SongPredictionResponse(**final_song_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

