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


    def __init__(self):
        self._prediction = {} 
        self.analyzed = False # state representing whether the data has been analyzed


    @abstractmethod
    def analyze_data(self, data):
        """
        Analyze the provided input data.

        Args:
            data (Data): The data object to be analyzed.
        
        """
        pass

    @property
    def prediction(self) -> dict:
        """
        Submit the partial solution to the blackboard.

        This allows other agents to consider the partial solution when attempting to 
        identify the song or provide recommendations.
        

        """

        if not self.analyze_data:
            raise ValueError("Data has not been analyzed yet.")
        
        return self._prediction
    

    @prediction.setter
    def prediction(self, prediction: dict):
        """
        Sets the prediction data by unpacking the dictionary.

        Args:
            prediction (dict): A dictionary containing prediction results.
        """
        if not isinstance(prediction, dict):
            raise TypeError("Prediction must be a dictionary")
        
        self._prediction = {**prediction}  # Unpacks and sets the dictionary
        self.analyzed = True



