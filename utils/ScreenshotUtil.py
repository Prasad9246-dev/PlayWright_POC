import allure

class ScreenshotUtil:
    def __init__(self, page):
        self.page = page

    def attach_screenshot(self, name="Screenshot"):
        """
        Takes a screenshot using the Playwright page object and attaches it to the Allure report.
        """
        screenshot_bytes = self.page.screenshot()
        allure.attach(
            screenshot_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def attach_text(self, text, name="Text Attachment"):
        """
        Attaches a text message to the Allure report.
        """
        allure.attach(
            text,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )