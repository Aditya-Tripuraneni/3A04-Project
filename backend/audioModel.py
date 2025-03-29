import vertexai
from google.oauth2 import service_account
from google import genai 
import os
import json
from google.genai import types



def classify_song(audio_file_path):
    # Get the path to the credentials file from the environment variable
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    print("GOOGLE_APPLICATION_CREDENTIALS:", credentials_path)

    # Load the credentials from the file
    if credentials_path and os.path.exists(credentials_path):
        try:
            with open(credentials_path, "r") as f:
                credentials_info = json.load(f)  # Read and parse the JSON file
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise  # Re-raise the exception to prevent the app from continuing
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set or file does not exist.")
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set or file does not exist.")

    # Initialize the genai.Client with credentials
    client = genai.Client(
        vertexai=True,
        project="songsnap-454217",
        location="us-central1",
        credentials=credentials
    )

    # Read the audio file from disk
    with open(audio_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    # Convert audio bytes to Part object
    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type="audio/mpeg"  # Adjust the MIME type if needed
    )

    model = "gemini-2.0-pro-exp-02-05"

    contents = [
        types.Content(
            role="user",
            parts=[
                audio_part,
                types.Part.from_text(
                    text="""Identify the song and the artist name, and state your confidence level in logarithmic probability.\n
                            Output the data in the form: "Name: Song Name Artist: Artist Name" Confidence: "Confidence" Do this on the same line."""
                )
            ]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=1,
        seed=0,
        max_output_tokens=2048,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
    )

    # Use the client to generate content
    client_models = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    response_text = ""
    for chunk in client_models:
        response_text += chunk.text if chunk.text else ""

    # Song result is in the form "Name: XXX Artist: YYY Confidence: ZZZ"
    return response_text