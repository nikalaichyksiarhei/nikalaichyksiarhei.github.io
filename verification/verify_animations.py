from playwright.sync_api import sync_playwright
import time

def verify_animations(page):
    page.goto("http://localhost:5173")
    page.wait_for_selector(".hero-content")

    # Scroll to features to trigger animations
    features = page.locator("#features")
    features.scroll_into_view_if_needed()

    # Wait for animation duration + delay (approx 2s)
    time.sleep(2.5)

    # Verify Analytics Graph
    # We expect stroke-dashoffset to be 0 after animation
    graph_path = page.locator(".anim-graph-path")

    # Get computed style
    offset = graph_path.evaluate("el => getComputedStyle(el).strokeDashoffset")
    print(f"Graph Stroke Dashoffset: {offset}")

    if offset == "0px" or offset == "0":
        print("PASS: Graph animation completed")
    else:
        print(f"FAIL: Graph animation did not complete (offset: {offset})")

    # Verify Widgets
    # We expect scale to be 1 and opacity 1
    widget = page.locator(".anim-widget-rect").first
    transform = widget.evaluate("el => getComputedStyle(el).transform")
    opacity = widget.evaluate("el => getComputedStyle(el).opacity")

    print(f"Widget Transform: {transform}")
    print(f"Widget Opacity: {opacity}")

    if opacity == "1" and transform != "none":
         print("PASS: Widget animation visible")
    else:
         print("FAIL: Widget animation issue")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_animations(page)
