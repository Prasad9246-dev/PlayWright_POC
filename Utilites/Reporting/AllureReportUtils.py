import subprocess
import os
from datetime import datetime

def run_pytest_with_allure(test_target=None):
    today = datetime.now().strftime("%Y-%m-%d")
    results_dir = os.path.join("allure-results", today)
    report_dir = os.path.join("allure-report", today, "html")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    pytest_cmd = f'python -m pytest --alluredir={results_dir} -v'
    if test_target:
        pytest_cmd += f' {test_target}'

    subprocess.run(pytest_cmd, shell=True, check=True)

    allure_cmd = f'allure generate {results_dir} -o {report_dir} --clean'
    subprocess.run(allure_cmd, shell=True, check=True)

    print(f"Allure HTML report generated at: {report_dir}")