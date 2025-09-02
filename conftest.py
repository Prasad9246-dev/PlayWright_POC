import pytest
from playwright.sync_api import sync_playwright
import tkinter as tk

@pytest.fixture(scope="function")
def setup():
    with sync_playwright() as p:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        screen_height = screen_height - 118 
        print(f"Screen width: {screen_width}, Screen height: {screen_height}")
        channel_name = "chrome"
        browser = p.chromium.launch(
            headless=False,
            channel=channel_name,
            args=["--start-fullscreen"]
        )
        # Set viewport=None to use the full window size
        context = browser.new_context(ignore_https_errors=True,viewport={"width": screen_width, "height": screen_height})
        page = context.new_page()
        yield page