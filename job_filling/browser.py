"""Connect to a running Chrome instance via Chrome DevTools Protocol."""

from __future__ import annotations

from playwright.async_api import Browser, Page, async_playwright

CDP_URL = "http://localhost:9222"


async def connect(cdp_url: str = CDP_URL) -> tuple[Browser, Page]:
    """Return (browser, active_page) connected over CDP.

    The caller is responsible for calling ``browser.close()`` when done
    (which only disconnects — it does NOT close the user's Chrome).
    """
    pw = await async_playwright().start()
    browser = await pw.chromium.connect_over_cdp(cdp_url)

    # Get the first browser context (the user's default profile)
    context = browser.contexts[0]
    pages = context.pages
    if not pages:
        raise RuntimeError("No open tabs found in the connected browser.")

    # Return the last (most recently focused) page
    page = pages[-1]
    return browser, page


async def wait_for_navigation(page: Page, timeout: float = 60_000) -> None:
    """Wait until the page URL or DOM changes (user clicked next page)."""
    old_url = page.url
    # Wait for either a navigation event or a significant DOM mutation
    try:
        await page.wait_for_url(lambda url: url != old_url, timeout=timeout)
    except Exception:
        # If URL didn't change, the page might have done an in-page update
        # (SPA navigation). We'll let the caller decide how to handle this.
        pass
