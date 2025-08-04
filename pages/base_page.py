class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a specific URL."""
        self.page.goto(url)

    def get_title(self):
        """Return the page title."""
        return self.page.title()
    
    def get_text(self, locator):
        """
        Returns the text content of the given locator.
        :param locator: a selector string or Playwright locator
        :return: The text content as a string, or None if not found.
        """
        try:
            return self.page.locator(locator).inner_text()
        except Exception:
            return None
