# Ecosystem Wave 2: Shared MCP Base And Scaffold Ergonomics

You are handling one workstream inside a larger Codex Cloud fanout for this repository.

Assume you are operating as a principal engineer with full autonomy to investigate this workstream.
You may inspect the repo deeply, run tests, prototype code, edit files, and use web or doc research when that materially improves the result.

## Objective

Improve the shared MCP base and package scaffold so the next packages we add are more ergonomic and more consistent by default.

## Why this workstream exists

The repo now has a shared `pydantic_ai_partner_mcp` base plus a scaffold script and templates. This is the leverage point for scaling the ecosystem. If the shared base or scaffold is awkward, every future package will inherit that awkwardness.

## Mode

- implementation
- investigate + implement + test

Compare a couple of plausible improvements, but make the highest-value changes you can justify.

## Operating assumptions

- Favor improvements that future packages inherit automatically.
- Keep the public surface small and coherent.
- If template defaults are too weak or misleading, fix them.
- If docs around the base package are insufficient, improve them.

## Required execution checklist

- You MUST inspect the base package, scaffold script, templates, and related tests.
- You MUST identify at least 3 concrete friction points for future package authors.
- You MUST implement the most valuable improvements.
- You MUST run the relevant tests/checks for changed files.
- You MUST explain how your changes improve future fanout safety and reduce merge conflicts.

## Required repo context

Read at least these:

- `packages/pydantic_ai_partner_mcp/README.md`
- `packages/pydantic_ai_partner_mcp/pydantic_ai_partner_mcp/_capability.py`
- `scripts/scaffold_partner_package.py`
- `templates/partner_mcp/README.md.tmpl`
- `templates/partner_mcp/package__capability.py.tmpl`
- `templates/partner_mcp/test_capability.py.tmpl`
- `tests/pydantic_ai_partner_mcp/test_partner_mcp_capability.py`
- `tests/test_scaffold_partner_package.py`

## Deliverable

Write one repo-local output at:

`reports/fanout/2026-04-23-ecosystem-wave-2/shared-base-hardening.md`

Also edit the repo where warranted and list changed files in the final note.

## Constraints

- prioritize inherited leverage over one-off fixes
- keep the API tasteful and minimal
- maintain type safety and test quality

## Success criteria

- Future packages would come out better by default after your changes.
- The scaffold and base package story is clearer and less error-prone.
- Test coverage around the shared base remains strong or improves.

## Decision style

End with:

- `Recommendation: <label>`
- `Main friction points: <short list>`
- `Changes made: <short list>`
- `What would change my mind: <specific evidence>`
