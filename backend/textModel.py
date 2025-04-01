import vertexai
from vertexai.generative_models import GenerativeModel
from .configurations import SAFTEY_SETTINGS, GENERATION_CONFIG
import os
import json
from google.oauth2 import service_account
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# I need a seperate model that can send audio files generate the code for this

def multiturn_generate_content(input_data):
    # Get the contents of the GOOGLE_APPLICATION_CREDENTIALS environment variable
    credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    logger.info("Credentials Loaded Successfully")

    # Load the credentials from the JSON string
    if credentials_json:
        try:
            credentials_info = json.loads(credentials_json)
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise  # Re-raise the exception to prevent the app from continuing

        # Use the credentials to authenticate with Google Cloud
        vertexai.init(
            project="songsnap-454217",
            location="us-central1",
            credentials=credentials,
            api_endpoint="us-central1-aiplatform.googleapis.com"
        )
        logger.info("Vertex AI Initialized Successfully")
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )

    logger.info("Model Loaded Successfully")
    chat = model.start_chat()

    # response from the model
    response = chat.send_message(
        [input_data],
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFTEY_SETTINGS
    )

    return response