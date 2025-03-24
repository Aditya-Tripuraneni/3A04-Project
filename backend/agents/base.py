from __future__ import annotations

import typing as t

import pydantic

Tin = t.TypeVar('Tin')
Tout = t.TypeVar('Tout')

RequestT = t.TypeVar('RequestT')
ResponseT = t.TypeVar('ResponseT')


class Identifier(pydantic.BaseModel, t.Generic[RequestT, ResponseT]):
  """Base class for all song identification methods."""

  # Class variables for endpoint names
  endpoint_name: t.ClassVar[str]

  # Method-specific data
  data: RequestT
  service: t.Any
  # Optional parameters
  num_suggestions: int = 5
  max_tokens: int = 4096
  temperature: float = 0.6
  seed: int = 0

  model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

  def identify_song(self) -> list[ResponseT]:
    """Identify a song via client asynchronously"""
    return getattr(self.service.to_sync, self.endpoint_name)(
      self.data,
      num_suggestions=self.num_suggestions,
      max_tokens=self.max_tokens,
      temperature=self.temperature,
      seed=self.seed,
    )

  async def async_identify_song(self) -> list[ResponseT]:
    """Identify a song via client asynchronously"""
    return await getattr(self.service, self.endpoint_name)(
      self.data,
      num_suggestions=self.num_suggestions,
      max_tokens=self.max_tokens,
      temperature=self.temperature,
      seed=self.seed,
    )

  @classmethod
  def from_data(cls, data: t.Any, service: t.Any, **kwargs: t.Any):
    return cls(data=cls._preprocess_inputs(data), service=service, **kwargs)

  @classmethod
  def _preprocess_inputs(cls, data: t.Any) -> RequestT:
    raise NotImplementedError('Subclasses should implement how to process data.')


class AgentState(pydantic.BaseModel, t.Generic[Tout]):
  score: float
  data: t.Optional[list[Tout]] = None
  analyzed: bool = pydantic.Field(default=False)

  def update_from_response(self, resp: list[Tout]):
    self.data = resp
    self.score = max(result.confidence for result in resp)
    self.analyzed = True


class Agent(pydantic.BaseModel, t.Generic[Tin, Tout]):
  """
  Abstract base class representing an Agent in the system.

  An Agent is responsible for analyzing input data, providing a confidence score,
  and submitting partial solutions to the blackboard. This allows different types of agents
  (e.g., audio, text, lyrical) to be created and used polymorphically.

  Methods:
      analyze_data(data): Analyze the provided data and extract meaningful insights.
      submit_partial_solution(): Submit the intermediate or final solution to the blackboard.
      get_confidence_score(): Return the confidence score of the analysis.
  """

  service: t.Any
  finder_cls: t.ClassVar[type[Identifier]]
  state: AgentState[Tout] = pydantic.Field(default_factory=lambda: AgentState(score=0.0))

  model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

  def analyze_data(self, data: t.Any, **kwargs: t.Any):
    """
    Analyze the provided input data.

    Args:
        data (t.Any): The data object to be analyzed.
    """
    finder = self.finder_cls.from_data(data, service=self.service, **kwargs)
    resp = finder.identify_song()
    self.state.update_from_response(resp)

  async def async_analyze_data(self, data: t.Any, **kwargs: t.Any):
    finder = self.finder_cls.from_data(data, service=self.service, **kwargs)
    resp = await finder.async_identify_song()
    self.state.update_from_response(resp)

  def get_confidence_score(self) -> float:
    """
    Return the confidence score of the analysis.

    Returns:
        float: A confidence score between 0 and 1.
    """
    if not self.state.analyzed:
      raise ValueError('Data is yet to be analyzed.')
    return self.state.score

  def submit_partial_solution(self):
    """
    Submit the partial solution to the blackboard.

    This allows other agents to consider the partial solution when attempting to
    identify the song or provide recommendations.
    """
    if not self.state.analyzed:
      raise ValueError('Data is yet to be analyzed.')
    return self.state.data
