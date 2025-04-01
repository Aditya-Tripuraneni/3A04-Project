from ..repositories.reportRepository import ReportRepository
from ..reportModels.report import Report

class ReportGenerator:
    def __init__(self, reportRepository: ReportRepository):
        self.reportRepository = reportRepository

    def generateAndSaveReport(self, report: Report):
        """
        Accepts a Report object (abstract class) and saves it to the database.
        Dynamically unpacks the attributes of the report.
        """
        if not isinstance(report, Report):
            raise TypeError("Expected a Report object.")

        # Convert the report to a dictionary using its `to_dict` method
        report_data = report.to_dict()

        # Save the report using the repository
        self.reportRepository.saveReport(report_data)