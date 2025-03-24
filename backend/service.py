from __future__ import annotations

import logging, pathlib, tempfile, typing as t
import bentoml, fastapi, pydantic, annotated_types as ae, typing_extensions as te

from contextlib import ExitStack, asynccontextmanager

from models import FromFileResponse, FromDescriptionResponse, FromLyricsResponse
from agents import AudioAnalyzer, DescriptionAnalyzer, LyricsAnalyzer
from agents.base import Agent
from libs import init_db, get_db_connection

with bentoml.importing():
  import google.genai.types as genai_types

  from google import genai

logger = logging.getLogger('bentoml.service')

MAX_TOKENS = 4096
WORKING_DIR = pathlib.Path(__file__).parent


class AppContext(t.TypedDict):
  analyzers: te.NotRequired[dict[str, Agent]]


app_context: AppContext = {}


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
  app_context['analyzers'] = {}
  yield
  # Clear the analyzers first
  if 'analyzers' in app_context:
    app_context['analyzers'].clear()


app = fastapi.FastAPI(title='API gateway', lifespan=lifespan)


@bentoml.asgi_app(app, path='/v1')
@bentoml.service(
  name='songsnap-rag',
  resources={'cpu': 4},
  traffic={'timeout': 300},
  image=bentoml.images.PythonImage(python_version='3.11', lock_python_packages=False).requirements_file(
    (WORKING_DIR / 'requirements.txt').__fspath__()
  ),
  envs=[
    # {"name": "GOOGLE_APPLICATION_CREDENTIALS", "value": (WORKING_DIR/'songsnap-454217-b12a994ae770.json').__fspath__()},
    {'name': 'UV_NO_PROGRESS', 'value': '1'},
    {'name': 'HF_HUB_DISABLE_PROGRESS_BARS', 'value': '1'},
  ],
  labels={'type': 'gateway', 'application': 'rag'},
)
class SnapRAG:
  gcp_project = 'songsnap-454217'
  gcp_location = 'us-central1'
  model = 'gemini-2.0-pro-exp-02-05'

  def __init__(self):
    self.stack = ExitStack()

  @bentoml.on_startup
  def init_resources(self):
    init_db()
    self.client = genai.Client(vertexai=True, project=self.gcp_project, location=self.gcp_location)
    self.conn = self.stack.enter_context(get_db_connection())

  @bentoml.on_shutdown
  def close_resources(self):
    self.stack.close()

  def create_config(
    self,
    schema: pydantic.BaseModel | type[t.Sequence[pydantic.BaseModel]],
    /,
    search: bool = True,
    *,
    temperature: float,
    max_tokens: int,
    seed: int = 0,
    **kwargs: t.Any,
  ) -> genai_types.GenerateContentConfig:
    tools = kwargs.get('tools', [])
    if search:
      tools.append(genai_types.Tool(google_search=genai_types.GoogleSearch()))

    return genai_types.GenerateContentConfig(
      temperature=temperature,
      seed=seed,
      max_output_tokens=max_tokens,
      safety_settings=[
        genai_types.SafetySetting(
          category=genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=genai_types.HarmBlockThreshold.OFF
        ),
        genai_types.SafetySetting(
          category=genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
          threshold=genai_types.HarmBlockThreshold.OFF,
        ),
        genai_types.SafetySetting(
          category=genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
          threshold=genai_types.HarmBlockThreshold.OFF,
        ),
        genai_types.SafetySetting(
          category=genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=genai_types.HarmBlockThreshold.OFF
        ),
      ],
      response_mime_type='application/json',
      response_schema=schema,
      tools=tools,
      **kwargs,
    )

  @bentoml.api
  async def from_file(
    self,
    audio_file: t.Annotated[pathlib.Path, bentoml.validators.ContentType('audio/mpeg')],
    *,
    num_suggestions: t.Annotated[int, ae.Ge(1)] = 5,
    max_tokens: t.Annotated[int, ae.Ge(128), ae.Le(MAX_TOKENS)] = MAX_TOKENS,
    temperature: t.Annotated[float, ae.Ge(0.2), ae.Le(1.0)] = 0.6,
    seed: int = 0,  # for max reproducibility
  ) -> list[FromFileResponse]:
    return sorted(
      t.cast(
        t.List[FromFileResponse],
        self.client.models.generate_content(
          model=self.model,
          contents=[
            genai_types.Content(
              role='user',
              parts=[
                genai_types.Part.from_bytes(data=audio_file.read_bytes(), mime_type='audio/mpeg'),
                genai_types.Part.from_text(
                  text=f'Identify the song and artist name from given audio file, and give your confidence level for each suggestion. Give at least {num_suggestions} suggestions.'
                ),
              ],
            )
          ],
          config=self.create_config(
            list[FromFileResponse], search=False, temperature=temperature, max_tokens=max_tokens, seed=seed
          ),
        ).parsed,
      ),
      key=lambda x: x.confidence,
      reverse=True,
    )

  @bentoml.api
  async def from_text(
    self,
    description: str = 'There is that one album by a female Icelandic singer that consists of jazz pop ballads, recently released in 2024.',
    *,
    num_suggestions: t.Annotated[int, ae.Ge(1)] = 5,
    max_tokens: t.Annotated[int, ae.Ge(128), ae.Le(MAX_TOKENS)] = MAX_TOKENS,
    temperature: t.Annotated[float, ae.Ge(0.2), ae.Le(1.0)] = 0.6,
    seed: int = 0,  # for max reproducibility
  ) -> list[FromDescriptionResponse]:
    return sorted(
      t.cast(
        t.List[FromDescriptionResponse],
        self.client.models.generate_content(
          model='gemini-2.0-pro-exp-02-05',
          contents=[
            genai_types.Content(
              role='user',
              parts=[
                genai_types.Part.from_text(
                  text=f"""Identify the song and artist name from the following description:
<description>
{description}
</description>
Give your confidence level for each suggestion. Give at least {num_suggestions} suggestions."""
                )
              ],
            )
          ],
          config=self.create_config(
            list[FromDescriptionResponse], search=False, temperature=temperature, max_tokens=max_tokens, seed=seed
          ),
        ).parsed,
      ),
      key=lambda x: x.confidence,
      reverse=True,
    )

  @bentoml.api
  async def from_lyrics(
    self,
    lyrics: str = """Floorboards creaking in my home
Deathly silence when alone
Oh, I wish that you were here right now
So, unlike me, somehow I
Fell in love in just three nights
Those November days still haunting me""",
    *,
    num_suggestions: t.Annotated[int, ae.Ge(1)] = 5,
    max_tokens: t.Annotated[int, ae.Ge(128), ae.Le(MAX_TOKENS)] = MAX_TOKENS,
    temperature: t.Annotated[float, ae.Ge(0.2), ae.Le(1.0)] = 0.6,
    seed: int = 0,  # for max reproducibility
  ) -> list[FromLyricsResponse]:
    return sorted(
      t.cast(
        t.List[FromLyricsResponse],
        self.client.models.generate_content(
          model=self.model,
          contents=[
            genai_types.Content(
              role='user',
              parts=[
                genai_types.Part.from_text(
                  text=f"""Identify the song and its artists given the following lyrics:
<lyrics>
{lyrics}
</lyrics>
Give your confidence level for each suggestion. Give at least {num_suggestions} suggestions."""
                )
              ],
            )
          ],
          config=self.create_config(
            list[FromLyricsResponse], search=False, temperature=temperature, max_tokens=max_tokens, seed=seed
          ),
        ).parsed,
      ),
      key=lambda x: x.confidence,
      reverse=True,
    )


class AnalyzeResponse(pydantic.BaseModel):
  audio: t.Optional[list[FromFileResponse]] = None
  description: t.Optional[list[FromDescriptionResponse]] = None
  lyrics: t.Optional[list[FromLyricsResponse]] = None


@app.post('/analyze', response_model=AnalyzeResponse)
async def analyze(
  audio_file: t.Optional[fastapi.UploadFile] = None,
  description: t.Optional[str] = None,
  lyrics: t.Optional[str] = None,
  *,
  num_suggestions: t.Annotated[int, ae.Ge(1)] = 5,
  max_tokens: t.Annotated[int, ae.Ge(128), ae.Le(MAX_TOKENS)] = MAX_TOKENS,
  temperature: t.Annotated[float, ae.Ge(0.2), ae.Le(1.0)] = 0.6,
  seed: int = 0,  # for max reproducibility
  service: SnapRAG = fastapi.Depends(bentoml.get_current_service),
) -> AnalyzeResponse:
  """Analyze audio, description or lyrics to identify songs using multiple analyzers."""
  response = AnalyzeResponse()
  analyzers = app_context.get('analyzers', {})

  # Get the endpoint URL for client connections
  common_params = {
    'num_suggestions': num_suggestions,
    'max_tokens': max_tokens,
    'temperature': temperature,
    'seed': seed,
  }

  # Process audio file if provided
  if audio_file is not None:
    if 'audio' not in analyzers:
      analyzers['audio'] = AudioAnalyzer(service=service)

    audio_analyzer = analyzers['audio']
    file_data = await audio_file.read()
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tf:
      tf.write(file_data)
      tf.flush()
      await audio_analyzer.async_analyze_data(pathlib.Path(tf.name), **common_params)
    response.audio = audio_analyzer.submit_partial_solution()

  # Process description if provided
  if description is not None:
    if 'description' not in analyzers:
      analyzers['description'] = DescriptionAnalyzer(service=service)

    description_analyzer = analyzers['description']
    await description_analyzer.async_analyze_data(description, **common_params)
    response.description = description_analyzer.submit_partial_solution()

  # Process lyrics if provided
  if lyrics is not None:
    if 'lyrics' not in analyzers:
      analyzers['lyrics'] = LyricsAnalyzer(service=service)

    lyrics_analyzer = analyzers['lyrics']
    await lyrics_analyzer.async_analyze_data(lyrics, **common_params)
    response.lyrics = lyrics_analyzer.submit_partial_solution()

  return response
