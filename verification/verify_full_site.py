from playwright.sync_api import sync_playwright
import time

def verify_full_site(page):
    page.goto("http://localhost:5173")
    page.wait_for_selector(".hero-content")

    # 1. Hero Parallax
    page.mouse.move(500, 500)
    time.sleep(1)
    page.screenshot(path="verification/final_hero.png")

    # 2. Features Animation
    features = page.locator("#features")
    features.scroll_into_view_if_needed()
    time.sleep(2) # Wait for animations
    page.screenshot(path="verification/final_features.png")

    print("Verification screenshots taken.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 1000})
        verify_full_site(page)
