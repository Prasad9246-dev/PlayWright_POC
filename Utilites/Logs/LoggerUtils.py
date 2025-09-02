import os
import inspect
from datetime import datetime
from Utilites.ExcelRead.ExcelReader import get_file_path

class LoggerUtils:
    def __init__(self, feature_name):
        self.feature_name = feature_name

    def log(self, message):
        """
        Logs a message to the test case log file in the folder structure: currentdate/featurename/testcasename.log
        Args:
            message (str): Log message to write.
        Author:
            Prasad Kamble
        """
        # Get test case name from stack
        excel_path = get_file_path("testCaseLogsPath")
        testcase_name = "unknown"
        for frame in inspect.stack():
            if frame.function.startswith("test_"):
                testcase_name = frame.function
                break
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(excel_path, current_date, self.feature_name)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{testcase_name}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")