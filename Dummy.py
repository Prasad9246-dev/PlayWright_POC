from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto('https://wdts-gateway-cs01.wdts.local:792/login')
        page.click("text=Username")
        page.fill("input[name='Username']", "ppmaster")
        page.press("input[name='Username']", "Tab")
        page.fill("input[name='Password']", "35Ramrod!")
        page.press("input[name='Password']", "Enter")
        page.click("button:has-text('Configuration v.2.6.3.0')")
        browser.close()

if __name__ == "__main__":
    run()