from abc import ABC, abstractmethod

class ReportRepository(ABC):
    @abstractmethod
    def saveReport(self, report):
        """Save a report to the database."""
        pass