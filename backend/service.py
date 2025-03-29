import traceback
from .controller import Controller
from .description import Description
from .lyrics import Lyrics
from .audio import Audio
from .models import AnalyzeRequest, SongPredictionResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import base64
import os
import tempfile
import sys

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

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
            audio_bytes = base64.b64decode(request.audio_request.audio_file)
            print("YALL I GOT A HIT!!!!!")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_bytes)
                tempfile_path = temp_file.name
        
            try:
                audio = Audio(tempfile_path)
                controller.analyze_data(audio)
            finally:
                os.remove(tempfile_path)

        final_song = controller.finalize_solution()
        final_song_data = final_song.get_song_data()

        return SongPredictionResponse(**final_song_data)
    except Exception as e:
        traceback.print_exc()
        logger.exception("An error occurred while processing the request")
        
        raise HTTPException(status_code=500, detail=str(e))

