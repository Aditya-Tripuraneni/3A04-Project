from __future__ import annotations

import pathlib

from agents.base import Agent, Identifier
from models.modality import Audio
from models.protocol import FromFileResponse


class AudioFinder(Identifier[pathlib.Path, FromFileResponse]):
  endpoint_name = 'from_file'

  @classmethod
  def _preprocess_inputs(cls, data: str | pathlib.Path | Audio) -> pathlib.Path:
    """Preprocess data inputs to get a file path.

    Handles string paths, Path objects, Audio model objects, and bytes objects.
    """
    # Handle different input types
    if isinstance(data, Audio):
      file_path = pathlib.Path(data.audio_file)
    elif isinstance(data, str):
      file_path = pathlib.Path(data)
    else:
      file_path = data

    # Ensure the file exists
    if not file_path.exists():
      raise FileNotFoundError(f'Audio file not found: {file_path}')
    return file_path


class AudioAnalyzer(Agent[pathlib.Path, list[FromFileResponse]]):
  finder_cls = AudioFinder
