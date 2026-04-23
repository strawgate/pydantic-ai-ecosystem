from __future__ import annotations

from mcp.server.fastmcp import FastMCP

browser = FastMCP(
    name='browser-test',
    instructions='Use the test browser tools to navigate pages and inspect their current state.',
)


@browser.tool()
def navigate_page(url: str) -> dict[str, str]:
    """Navigate to a page and report a stable title for tests."""
    return {
        'url': url,
        'title': 'Example Page',
        'status': 'loaded',
    }


@browser.tool()
def snapshot_page() -> dict[str, object]:
    """Capture a stable page snapshot for tests."""
    return {
        'title': 'Example Page',
        'heading': 'Welcome',
        'links': ['Docs', 'Pricing'],
    }


def main() -> None:
    browser.run()


if __name__ == '__main__':
    main()
