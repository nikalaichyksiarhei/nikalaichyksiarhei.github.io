from playwright.sync_api import sync_playwright
import time

def verify_visuals(page):
    page.goto("http://localhost:5173")
    page.wait_for_selector(".hero-content")

    # 1. Parallax Screenshot
    # Move mouse to force tilt
    page.mouse.move(100, 100)
    time.sleep(0.5)
    page.screenshot(path="verification/parallax_visual.png")

    # 2. Spotlight Screenshot
    # Scroll to features
    features = page.locator("#features")
    features.scroll_into_view_if_needed()

    # Hover over first card
    card = page.locator(".feature-card").first
    box = card.bounding_box()
    # Move to center of card
    page.mouse.move(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    time.sleep(0.5)

    page.screenshot(path="verification/spotlight_visual.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        verify_visuals(page)
