from blackboardkeys import FactKeys
from data import Data


class BlackBoard:
    def __init__(self):
        self.data = {}
        self.partial_solutions = {}


    def write_data(self, key: FactKeys, value: Data):
        self.data[key] = value
        
    def read_data(self, key: FactKeys) -> Data:
        return self.data.get(key)
        
    def write_solution(self, key: FactKeys, value: Data):
        self.partial_solutions[key] = value
        
    def read_solution(self, key:FactKeys) -> Data:
        return self.partial_solutions.get(key)
        
