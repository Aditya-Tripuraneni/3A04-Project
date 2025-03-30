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

logging.basicConfig(level=logging.DEBUG)
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
        logger.info("Starting /analyze_song endpoint")

        controller = Controller()

        if request.lyrics_request:
            lyrics = Lyrics(request.lyrics_request.lyrics)
            controller.analyze_data(lyrics)
            
        if request.description_request:
            description = Description(**request.description_request.model_dump())
            controller.analyze_data(description)

        if request.audio_request:
            logging.info("Processing audio request")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                logger.info(f"Temporary audio file created at: {temp_file.name}")
                base_64_data = request.audio_request.audio_file

                CHUNK_SIZE = 1024 * 1024  # 1 MB
                for i in range(0, len(base_64_data), CHUNK_SIZE):
                    chunk = base_64_data[i:i + CHUNK_SIZE]
                    temp_file.write(base64.b64decode(chunk))
                    temp_file.flush()
                
                tempfile_path = temp_file.name
            
            try:
                audio = Audio(tempfile_path)
                logging.info("Audio object created successfully")
                controller.analyze_data(audio)
                logging.info("Audio data analyzed successfully")
            finally:
                if os.path.exists(tempfile_path):
                    os.remove(tempfile_path)
                    logger.info(f"Temporary audio file deleted: {tempfile_path}")

        logger.info("Finalizing solution")
        final_song = controller.finalize_solution()
        final_song_data = final_song.get_song_data()
        logger.info("Returning final song data")

        return SongPredictionResponse(**final_song_data)
    except Exception as e:
        traceback.print_exc()
        logger.exception("An error occurred while processing the request")
        
        raise HTTPException(status_code=500, detail=str(e))

