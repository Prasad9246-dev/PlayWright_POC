import pytest
from playwright.sync_api import sync_playwright
from utils.excel_reader import read_excel_config

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
        tear_down_browser(browser)


def get_config():
    return read_excel_config("data/config_data.xlsx")

config = get_config()


def get_tableIP():
    table_ip = config.get("tableip")
    print(table_ip)
    return table_ip


def get_username():
    return config.get("username")


def get_password():
    return config.get("password")


def get_env():
    return config.get("env")

def get_ppApplication_Url():
    url_template = config.get("ppapplicationurl")  # use lowercase key
    env = config.get("env")
    print(f"url_template: {url_template}, env: {env}")
    if url_template and env:
        return url_template.replace("env", env)
    print(url_template)
    return url_template

def get_url():
    url_template = config.get("url")
    table_ip = config.get("tableip")
    if url_template and table_ip:
        # Replace 'tableIP' in the string with the actual IP
        return url_template.replace("tableIP", table_ip)
    print(url_template)
    return url_template

def tear_down_browser(browser):
    """Closes the browser and prints a message."""
    try:
        browser.close()
        print(" Browser closed. Teardown complete.")
    except Exception as e:
        print(f"Error closing browser: {e}")
        
if __name__ == "__main__":
    url = get_ppApplication_Url()
    print(f"PP Application URL: {url}")