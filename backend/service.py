import traceback

from .artistBasedRecommender import ArtistBasedRecommender

from .repositories.firestoreReportRepository import FirestoreReportRepository
from .reportModels.songIdentificationReport import SongIdentificationReport
from .generators.reportGenerator import ReportGenerator
from .database.databaseRepository import db


from .controller import Controller
from .description import Description
from .lyrics import Lyrics
from .audio import Audio
from .models import AnalyzeRequest, PredictedSong, SongPredictionResponse, LogTransactionRequest
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import base64
import os
import tempfile

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
            logging.info("Processing Lyrics")
            lyrics = Lyrics(request.lyrics_request.lyrics)
            controller.analyze_data(lyrics)
            
        if request.description_request:
            logging.info("Processing Description")
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

        reccomender = ArtistBasedRecommender(final_song)
        recommended_songs = reccomender.recommend_songs()
        logger.info("Recommended songs generated successfully")
        logger.info(f"Recommended songs: {recommended_songs}")



        return SongPredictionResponse(predicted_song= PredictedSong(**final_song_data), 
                                      recommended_songs=recommended_songs
                                    )  
        

    except Exception as e:
        traceback.print_exc()
        logger.exception("An error occurred while processing the request")
        
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/log_system_transaction")
async def log_system_transaction(data: LogTransactionRequest):
    """
    Logs the system transaction data.
    """
    logger.info("Starting /log_system_transaction endpoint")
    logger.info(f"Received data: {data.model_dump()}")
    try:
        logger.info("Starting /log_system_transaction endpoint")
        repository = FirestoreReportRepository(db)
        generator = ReportGenerator(repository)
        logger.info("FirestoreReportRepository and ReportGenerator initialized successfully")
        logger.debug(f"Incoming data: {data}")

        # Create a SongIdentificationReport object from the incoming data
        report = SongIdentificationReport(**data)
        
        # Generate and save the report
        generator.generateAndSaveReport(report)
        logger.info("Report generated and saved successfully")

        return {"message": "Transaction logged successfully"}
    except Exception as e:
        traceback.print_exc()
        logger.exception("An error occurred while logging the transaction")
        raise HTTPException(status_code=500, detail=str(e))

