from playwright.sync_api import sync_playwright
import time

def verify_effects(page):
    # Navigate
    page.goto("http://localhost:5173")

    # Wait for content
    page.wait_for_selector(".hero-content")

    # --- Verify Parallax ---
    # Move mouse to top-left to trigger parallax
    page.mouse.move(0, 0)
    time.sleep(0.5)

    # Check style of phones-container
    container = page.locator(".phones-container")
    style = container.get_attribute("style")
    print(f"Container Style (0,0): {style}")

    # Assert transform is present
    if "transform" not in style:
        print("FAIL: Parallax transform not found on .phones-container")
    else:
        print("PASS: Parallax transform detected")

    # --- Verify Spotlight ---
    # Scroll to features
    features = page.locator("#features")
    features.scroll_into_view_if_needed()

    # Get a card
    card = page.locator(".feature-card").first
    box = card.bounding_box()

    # Move mouse over card
    page.mouse.move(box["x"] + 10, box["y"] + 10)
    time.sleep(0.5)

    # Check CSS vars
    card_style = card.get_attribute("style")
    print(f"Card Style (Hover): {card_style}")

    if "--mouse-x" in card_style and "--mouse-y" in card_style:
         print("PASS: Spotlight CSS vars detected")
    else:
         print("FAIL: Spotlight CSS vars missing")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Set viewport to desktop size
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            verify_effects(page)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
