# Pydantic AI Playwright

Implementation package for Playwright capability integrations.

Initial direction:

- `PlaywrightCapability` as the primary surface
- MCP-backed defaults with browser-oriented instructions
- a clean path to deeper workflow logic later

This package should become the default Playwright partner capability for Pydantic AI agents.

## Testing

The package should be verifiable without manual testing:

- fast construction and spec tests
- local MCP inventory tests against a browser-shaped test server
- deterministic agent tests for safe browser-read flows
- an opt-in smoke test against the real `@playwright/mcp` server

Enable the real MCP smoke test with `PYDANTIC_AI_RUN_PLAYWRIGHT_MCP_TESTS=1`.
