from applitools.playwright import Eyes, Target
from playwright.sync_api import sync_playwright

def test_visual_ui(test_name: str):
    # Initialize Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Initialize Applitools Eyes
        eyes = Eyes()

        # Start test
        eyes.open(
            driver=page,
            app_name='AI Automation Demo',
            test_name=str(test_name),
            viewport_size={'width': 1800, 'height': 1200}
        )

        # Navigate to website
        page.goto("https://demo.applitools.com")

        # Visual checkpoint 1 → Login Page
        eyes.check("Login Page", Target.window().fully())

        # Perform login
        page.fill('#username', 'test_user')
        page.fill('#password', 'password')
        page.click('#log-in')

        # Visual checkpoint 2 → Dashboard
        eyes.check("Dashboard", Target.window().fully())

        # Close Eyes
        eyes.close_async()

        browser.close()
