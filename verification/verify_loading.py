from playwright.sync_api import sync_playwright
import time

def verify(page):
    # Navigate
    page.goto("http://localhost:5173")

    # Wait for hero content
    page.wait_for_selector(".hero-content")

    # Scroll to phones container to trigger lazy load
    phones_container = page.locator(".phones-container")
    phones_container.scroll_into_view_if_needed()

    # Wait a bit for images to load (lazy load)
    # Since we optimized images and local net is fast, they might load instantly.
    time.sleep(2)

    # Take screenshot of the phones
    page.screenshot(path="verification/verification.png")

    print("Screenshot taken")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify(page)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
