# from playwright.sync_api import sync_playwright

# def open_dashboard():
#     with sync_playwright() as p:
#         # Launch Chromium with full screen (maximize)
#         browser = p.chromium.launch(
#             headless=False,
#             args=["--start-maximized"]
#         )
        
#         # Create context with viewport=None to use full available screen size
#         context = browser.new_context(
#             ignore_https_errors=True,
#             viewport=None
#         )
        
#         page = context.new_page()
#         page.goto("https://172.31.3.83:790/tabledashboard")
#         print("Player page opened successfully.")

#         # Login steps
#         page.get_by_text('Username').click()
#         page.get_by_role('textbox', name='Username').fill('ppmaster')
#         page.get_by_role('textbox', name='Username').press('Tab')
#         page.get_by_role('textbox', name='Password').fill('35Ramrod!')
#         page.get_by_role('button', name='Login').click()
#         page.get_by_role('button', name='arrow_drop_down', exact=True).click()
#         page.get_by_role('menuitem', name='Close').click()
#         page.get_by_role('button', name='Confirm').click()
#         page.get_by_role('button', name='arrow_drop_down', exact=True).click()
#         page.get_by_role('menuitem', name='Open').click()
#         page.get_by_role('button', name='Confirm').click()

#         page.wait_for_timeout(5000)  # Wait for observation
#         browser.close()

# # Execute the function
# open_dashboard()

# import { test, expect } from '@playwright/test';

# test.use({
#   ignoreHTTPSErrors: true
# });

# test('test', async ({ page }) => {
#   await page.goto('https://172.31.3.83:790/tabledashboard/2025-07-28/player');
#   await page.locator('section').filter({ hasText: '1' }).locator('div').first().click();
#   await page.getByRole('textbox', { name: 'Player Search' }).fill('6001');
#   await page.getByRole('textbox', { name: 'Player Search' }).press('Enter');
#   await page.getByRole('button').filter({ hasText: /^$/ }).nth(1).click();
# });
