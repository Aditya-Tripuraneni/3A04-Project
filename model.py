import vertexai
from vertexai.generative_models import GenerativeModel
from configurations import SAFTEY_SETTINGS, GENERATION_CONFIG

# I need a seperate model that can send audio files generate the code for this



def multiturn_generate_content(input_data):
    vertexai.init(
        project="songsnap-454217",
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )
    chat = model.start_chat()

    # response from the model
    response = chat.send_message(
        [input_data],
        generation_config= GENERATION_CONFIG,
        safety_settings = SAFTEY_SETTINGS
        )
    
    return response




