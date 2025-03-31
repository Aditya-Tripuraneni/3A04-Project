from reportRepository import ReportRepository



class FirestoreReportRepository(ReportRepository):
    def __init__(self, db):
        self.db = db

    def saveReport(self, report):
        if not isinstance(report, dict):
            report = report.to_dict()
            
        collection_ref = self.db.collection("reports")
        collection_ref.add(report)
        print("Report saved successfully.")