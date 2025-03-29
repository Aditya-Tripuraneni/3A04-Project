from google import genai
from google.genai import types
import base64

def classify_song(base64_audio):
    client = genai.Client(
        vertexai=True,
        project="songsnap-454217",
        location="us-central1",
    )

    # Convert base64 audio data to Part object
    audio_part = types.Part.from_bytes(
        data=base64.b64decode(base64_audio),
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


