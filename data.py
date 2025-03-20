from abc import ABC, abstractmethod

class Data(ABC):
    """
    Abstract base class representing a piece of data.

    This class defines a contract for how data should be structured and stored.
    Subclasses must implement the `_store_data` method, which defines how the data 
    should be persisted or processed.

    The _store_data is a protected method denoting it should not be used outside of the class itself. 
    """

    @abstractmethod
    def _store_data(self):
        """
        Define how the data should be stored.

        This method must be implemented by any subclass to define the specific 
        storage mechanism for that type of data.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        pass
