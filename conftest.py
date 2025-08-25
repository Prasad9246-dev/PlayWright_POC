import pytest
from playwright.sync_api import sync_playwright
from utils.TestReportWriter import TestReportWriter
from utils.config_read import ConfigUtils
from datetime import datetime
import tkinter as tk

@pytest.fixture(scope="function")
def setup():
    with sync_playwright() as p:
        screen_width = tk.Tk().winfo_screenwidth()
        screen_height = tk.Tk().winfo_screenheight()
        browser = p.chromium.launch(
            headless=False,
            channel="chrome", # Use the Edge browser msedge
            args=["--start-maximized"]
        )
        # Set viewport=None to use the full window size
        context = browser.new_context(ignore_https_errors=True,viewport={"width": screen_width, "height": screen_height})
        page = context.new_page()
        # page.set_viewport_size({"width": screen_width, "height": screen_height})
        yield page

def pytest_runtest_makereport(item, call):
    # Only act after the test call phase
    if call.when == "call":
        tbd = getattr(item, "tbd", None)
        # Get test case ID (function name or nodeid)
        raw_id = item.name if hasattr(item, "name") else item.nodeid.split("::")[-1]
        test_case_id = raw_id.replace("test_", "TEST-")
        print(f"Test case ID: {test_case_id}")
        # Determine status and remarks
        if call.excinfo is not None:
            status = "Fail"
            remarks = str(call.excinfo.value)
            if tbd:
                try:
                    tbd.void_game()
                except Exception as e:
                    print(f"Failed to void hand in hook: {e}")
        else:
            status = "Pass"
            remarks = ""
        # Write test case report
        config_utils = ConfigUtils()
        config = config_utils.get_config()
        BUILD_VERSION = config.get("build_version")
        FEATURE_NAME = config.get("feature_name")
        report_writer = TestReportWriter(BUILD_VERSION, FEATURE_NAME)
        report_writer.add_result(
            test_set_name=FEATURE_NAME,
            test_case_id=test_case_id,
            status=status,
            remarks=remarks,
            time_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        report_writer.write_report()
           
if __name__ == "__main__":
    pass