from song import Song
from blackboardkeys import FactKeys, PartialSolutionKeys
from data import Data


class BlackBoard:
    def __init__(self):
        self.data = {}
        self.partial_solutions = {}
        self.solved_state = False


    def write_fact(self, key: FactKeys, value: Data):
        self.data[key] = value
        
    def read_fact(self, key: FactKeys) -> Data:
        return self.data.get(key)
        
    def write_partial_solution(self, key: PartialSolutionKeys, value: Data):
        self.partial_solutions[key] = value
        
    def read_partial_solution(self, key:PartialSolutionKeys) -> Data:
        return self.partial_solutions.get(key)
    
    def finalize_solution(self) -> Song:
        self.solved_state = True
        # return the song with the highest confidence score from the partial solutions
        song = max(self.partial_solutions.values(), key=lambda data: data.confidence_score)
        return song

