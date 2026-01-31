from playwright.sync_api import sync_playwright
import time

def verify_visuals(page):
    page.goto("http://localhost:5173")
    page.wait_for_selector(".hero-content")

    # Scroll to features
    features = page.locator("#features")
    features.scroll_into_view_if_needed()

    # Wait for animations to finish
    time.sleep(2)

    page.screenshot(path="verification/animations_visual.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        verify_visuals(page)
