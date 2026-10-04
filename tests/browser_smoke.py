"""Exercise the deployed JavaScript in Chromium and WebKit on the built site."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import sys

from playwright.sync_api import expect, sync_playwright


def check_browser(browser_type, origin, site_url, jquery_version):
    browser = browser_type.launch()
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, color_scheme="light")
    errors = []

    # Jekyll emits absolute production URLs. Serve those requests from the local
    # artifact so we test the new build, never the currently deployed website.
    def serve_artifact(route):
        url = route.request.url
        if not url.startswith(site_url + "/"):
            route.abort()
            return
        response = context.request.get(origin + url[len(site_url):])
        if not response.ok:
            errors.append(f"{url}: HTTP {response.status}")
        route.fulfill(response=response)

    context.route("**/*", serve_artifact)
    page = context.new_page()
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(site_url + "/", wait_until="networkidle")
    expect(page.locator("#site-nav")).to_be_visible()
    page.wait_for_function("version => window.jQuery && window.jQuery.fn.jquery === version", arg=jquery_version)
    expect(page.locator("#site-nav .hidden-links > li")).to_have_count(0)
    link_count = page.locator("#site-nav li").count()

    # Moving between desktop and mobile must preserve every navigation item.
    page.set_viewport_size({"width": 390, "height": 844})
    nav_toggle = page.locator(".greedy-nav__toggle")
    hidden_links = page.locator("#site-nav .hidden-links")
    expect(nav_toggle).to_be_visible()
    nav_toggle.click()
    expect(nav_toggle).to_have_attribute("aria-expanded", "true")
    expect(hidden_links).to_be_visible()
    assert hidden_links.locator("li").count() > 0
    nav_toggle.click()
    expect(nav_toggle).to_have_attribute("aria-expanded", "false")
    expect(hidden_links).to_be_hidden()
    assert page.locator("#site-nav li").count() == link_count

    follow = page.locator(".author__urls-wrapper > button")
    social_links = page.locator(".author__urls")
    expect(follow).to_be_visible()
    expect(social_links).to_be_hidden()
    follow.click()
    expect(social_links).to_be_visible()
    follow.click()
    expect(social_links).to_be_hidden()

    theme = page.locator("#theme-toggle button")
    theme.click()
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    assert page.evaluate("localStorage.getItem('theme')") == "dark"
    page.reload(wait_until="networkidle")
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    theme.click()
    expect(page.locator("html")).not_to_have_attribute("data-theme", "dark")
    assert page.evaluate("localStorage.getItem('theme')") == "light"

    page.set_viewport_size({"width": 1920, "height": 1080})
    expect(nav_toggle).to_be_hidden()
    expect(hidden_links.locator("li")).to_have_count(0)
    expect(social_links).to_be_visible()
    assert page.locator("#site-nav li").count() == link_count

    page.goto(site_url + "/publications/", wait_until="networkidle")
    page.wait_for_function("version => window.jQuery && window.jQuery.fn.jquery === version", arg=jquery_version)
    expect(page.locator("#site-nav")).to_be_visible()
    assert not errors, "Browser JavaScript errors: " + "; ".join(errors)
    print(f"{browser_type.name}: jQuery {jquery_version}, navigation, resizing, Follow, theme and publications passed")
    context.close()
    browser.close()


if __name__ == "__main__":
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    lockfile = Path(__file__).resolve().parent.parent / "package-lock.json"
    jquery_version = json.loads(lockfile.read_text())["packages"]["node_modules/jquery"]["version"]
    site_url = json.loads((lockfile.parent / "package.json").read_text())["homepage"].rstrip("/")
    assert (site / "index.html").is_file(), "Build the Jekyll site before running browser tests"
    handler = partial(SimpleHTTPRequestHandler, directory=str(site))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            origin = f"http://127.0.0.1:{server.server_port}"
            for browser_type in (playwright.chromium, playwright.webkit):
                check_browser(browser_type, origin, site_url, jquery_version)
    finally:
        server.shutdown()
        server.server_close()
