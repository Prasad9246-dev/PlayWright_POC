import pytest
from playwright.sync_api import sync_playwright, Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"ignore_https_errors": True}


@pytest.fixture(scope="function")
def page_chrome():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_example(page_chrome: Page) -> None:
    page = page_chrome
    page.goto("https://172.31.3.83:790/login/table-ui")
    page.get_by_text("Username").click()
    page.get_by_role("textbox", name="Username").fill("ppmaster")
    page.get_by_text("Password").click()
    page.get_by_role("textbox", name="Password").fill("35Ramrod!")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="arrow_drop_down", exact=True).click()
    page.get_by_role("menuitem", name="Close").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_text("Table is closed").click()
    page.get_by_role("button", name="arrow_drop_down", exact=True).click()
    page.get_by_role("menuitem", name="Open").click()
    page.get_by_role("button", name="Confirm").click()