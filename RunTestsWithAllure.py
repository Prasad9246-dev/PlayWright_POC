import sys
from Utilites.Reporting.AllureReportUtils import run_pytest_with_allure

if __name__ == "__main__":
    # If argument is given, run that test; else run all tests in 'tests' folder
    test_target = sys.argv[1] if len(sys.argv) > 1 else None
    run_pytest_with_allure(test_target)