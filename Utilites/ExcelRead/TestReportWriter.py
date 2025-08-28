import os
import getpass
from datetime import datetime
from openpyxl import Workbook, load_workbook

class TestReportWriter:
    def __init__(self, build_version, feature_name):
        self.username = getpass.getuser()
        self.build_version = build_version
        self.feature_name = feature_name
        self.date_str = datetime.now().strftime("%Y-%m-%d")
        # self.folder_path = rf"C:\Users\{self.username}\Walker Digital Table Systems\WDTS INDIA - automation\Playwright\TestCaseReport"
        self.test_case_report_path = r"C:\Users\chiac\Walker Digital Table\u00A0Systems\WDTS INDIA - automation\Playwright\TestCaseReport"
        self.test_case_report_path = self.test_case_report_path.replace(r'\u00A0', '\u00A0')
        self.folder_path = os.path.join(self.test_case_report_path, self.date_str)
        os.makedirs(self.folder_path, exist_ok=True)
        self.file_name = f"{self.build_version}_{self.date_str}.xlsx"
        self.file_path = os.path.join(self.folder_path, self.file_name)
        self.results = []

    def add_result(self, test_set_name, test_case_id, status, remarks, time_str):
        """
        Adds a test result to the report.
        Author:
            Prasad Kamble
        """
        self.results.append({
            "test_set_name": test_set_name,
            "test_case_id": test_case_id,
            "status": status,
            "remarks": remarks,
            "time": time_str
        })

    def write_report(self):
        """
        Writes the test report to an Excel file.
        Author:
            Prasad Kamble
        """
        if os.path.exists(self.file_path):
            wb = load_workbook(self.file_path)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "TestCaseReport"
            # Write header only if new file
            ws.append(["Test Set Name", "Test case ID", "Status", "Remarks", "Time"])
        # Append new results
        for result in self.results:
            ws.append([
                result["test_set_name"],
                result["test_case_id"],
                result["status"],
                result["remarks"],
                result["time"]
            ])
        wb.save(self.file_path)
        print(f"Test report written to: {self.file_path}")      