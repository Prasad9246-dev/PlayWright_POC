import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="chrome", # Use the Edge browser msedge
            args=["--start-maximized"]
        )
        # Set viewport=None to use the full window size
        context = browser.new_context(ignore_https_errors=True,viewport={"width": 1366, "height": 650})
        page = context.new_page()
        yield page

def pytest_runtest_makereport(item, call):
    # Only act after the test call phase
    if call.when == "call" and call.excinfo is not None:
        base_test = getattr(item, "base_test", None)
        if base_test:
            try:
                base_test.void_game()
            except Exception as e:
                print(f"Failed to void hand in hook: {e}")
           
if __name__ == "__main__":
    pass