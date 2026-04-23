# Ecosystem Governance

This repo should optimize for integrations we can verify automatically before a human ever does a manual smoke test.

## Admission Bar

An integration should not become a real package unless it clears all of these:

- There is a clear reason to exist beyond raw `MCP(...)`.
- The package can describe a concrete automated verification strategy.
- The package can be published independently with narrow runtime dependencies.
- The package has a small, obvious public API.

If a candidate only amounts to `MCP(url=...)` with no useful defaults, it probably belongs in docs rather than as a package.

## Verification Levels

We prioritize integrations by the strongest automated test we believe we can run in CI:

1. `spec_only`
   - Import, spec construction, and serialization only.
2. `transport_smoke`
   - Start the server or client and assert the connection succeeds.
3. `inventory`
   - Assert real tool discovery and a stable subset of tool metadata.
4. `read_roundtrip`
   - Execute at least one real read-only tool call.
5. `write_roundtrip`
   - Execute a real isolated mutation and assert the resulting state.

Packages in the first wave should generally reach `read_roundtrip` or `write_roundtrip`.

## Auth Tiers

These tiers heavily affect priority:

- `none`
  - No credentials required.
- `local`
  - Local-only runtime such as Docker or a pinned local service.
- `service_token`
  - A stable machine credential can drive CI.
- `oauth_user`
  - Requires a human account connection or interactive consent.

`none`, `local`, and `service_token` are acceptable for early work. `oauth_user` should usually wait.

## Delivery Tiers

- `mcp_baseline`
  - Thin capability over an MCP server with good defaults.
- `opinionated_capability`
  - MCP plus prompts, filtering, approval rules, or workflow conventions.
- `full_backend`
  - Custom backend logic or direct SDK integration.

The default path is `mcp_baseline` or `opinionated_capability`. `full_backend` should be rare.

## Initial Waves

- Wave 1
  - No human smoke test required.
  - Strong CI story.
  - Prefer `read_roundtrip` or better.
- Wave 2
  - Needs service tokens or more partner-specific setup.
  - Still realistic to verify automatically.
- Incubating
  - OAuth-heavy or manual setup.
  - Keep as proposals or thin scaffolds until the test story improves.

## Current Rule

When in doubt, prioritize the integration with the better automated verification path, not the bigger brand name.
