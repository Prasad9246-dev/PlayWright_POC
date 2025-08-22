from playwright.sync_api import sync_playwright
import tkinter as tk

def run():
    with sync_playwright() as p:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.set_viewport_size({"width": screen_width, "height": screen_height})
        page.goto('https://wdts-gateway-cs01.wdts.local:792/login')
        page.get_by_role("textbox", name="Username").fill("ppmaster")
        page.get_by_role("textbox", name="Password").fill("35Ramrod!")
        page.get_by_role("textbox", name="Password").press("Enter")
        page.get_by_role("button", name="Configuration v.2.6.3.0").click()
        # browser.close()


if __name__ == "__main__":
    pass
    # run()