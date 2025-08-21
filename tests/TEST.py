import { test, expect, Page, BrowserContext } from '@playwright/test';

// Reusable login function
async function login(page: Page, username: string, password: string) {
  await expect(page.getByText('Login')).toBeVisible();
  await page.getByRole('textbox', { name: 'Username' }).fill(username);
  await page.getByRole('textbox', { name: 'Password' }).fill(password);
  await page.getByRole('textbox', { name: 'Password' }).press('Enter');
  await page.getByRole('button', { name: 'Submit' }).click();
}

// Reusable function to click Configuration button (dynamic version)
async function clickConfiguration(page: Page) {
  const configButton = page.getByRole('button', { name: /Configuration/ });
  await expect(configButton).toBeVisible();
  await configButton.click();
}

// Reusable function to open Game Templates tab
async function openGameTemplatesTab(page: Page) {
  const gameTemplatesTab = page.getByRole('tab', { name: 'Game Templates' });
  await expect(gameTemplatesTab).toBeVisible();
  await gameTemplatesTab.click();
}

// Reusable function to open a new page and navigate to Game Templates URL
async function openGameTemplatesPage(context: BrowserContext, url: string) {
  const newPage = await context.newPage();
  await newPage.goto(url);
  await expect(newPage).toHaveURL(url);
  return newPage;
}

test('test', async ({ page, context }) => {
  await login(page, 'ppmaster', '35Ramrod!');
  await clickConfiguration(page);
  await openGameTemplatesTab(page);

  // Open Game Templates in new tabs
  const gameTemplatesUrl = 'https://wdts-gateway-cs01.wdts.local:796/configuration/game-templates';
  const page1 = await openGameTemplatesPage(context, gameTemplatesUrl);
  const page2 = await openGameTemplatesPage(context, gameTemplatesUrl);
});