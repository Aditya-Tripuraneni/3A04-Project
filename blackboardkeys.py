from enum import Enum

class FactKeys(Enum):
    # BLACKBOARD FACT KEYS
    AUDIO_FILE = "audio_file"
    LYRICAL_TEXT = "lyrical_text"
    DESCRIPTION_TEXT = "description_text"

class PartialSolutionKeys(Enum):
    # PARTIAL SOLUTION KEYS
    AUDIO_FILE = "audio_file"
    LYRICAL_RESULT = "lyrical_result"
    DESCRIPTION_RESULT = "description_result"
