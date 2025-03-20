from abc import ABC, abstractmethod

class Agent(ABC):
    """
    Abstract base class representing an Agent in the system.

    An Agent is responsible for analyzing input data, providing a confidence score, 
    and submitting partial solutions to the blackboard. This allows different types of agents 
    (e.g., audio, text, lyrical) to be created and used polymorphically.

    Methods:
        analyze_data(data): Analyze the provided data and extract meaningful insights.
        get_confidence_score(): Return the confidence score of the analysis.
        submit_partial_solution(): Submit the intermediate or final solution to the blackboard.
    """

    @abstractmethod
    def analyze_data(self, data):
        """
        Analyze the provided input data.

        Args:
            data (Data): The data object to be analyzed.
        
        """
        pass

    @abstractmethod
    def get_confidence_score(self):
        """
        Return the confidence score of the analysis.

        Returns:
            float: A confidence score between 0 and 1.
        
        """
        pass

    @abstractmethod
    def submit_partial_solution(self):
        """
        Submit the partial solution to the blackboard.

        This allows other agents to consider the partial solution when attempting to 
        identify the song or provide recommendations.
        

        """
        pass
