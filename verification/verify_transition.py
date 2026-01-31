from playwright.sync_api import sync_playwright
import time

def verify_transition(page):
    page.goto("http://localhost:5173")
    page.wait_for_selector(".hero-content")

    # Scroll to the bottom of the hero section to see the transition
    # The transition is at the bottom of the hero
    # Phones container height is 600px, top padding 160px.
    # Let's scroll to around 700px.
    page.evaluate("window.scrollTo(0, 500)")
    time.sleep(1) # Wait for any animations

    page.screenshot(path="verification/transition_visual.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 1000}) # Taller viewport
        verify_transition(page)
