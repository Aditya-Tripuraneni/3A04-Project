from agents import Agent
from data import Data


class DescriptionAnalyzer(Agent):

    def analyze_data(self, data: Data):
        pass

    def get_confidence_score(self):
        return 0.5
    
    def submit_partial_solution(self):
        return 6
    