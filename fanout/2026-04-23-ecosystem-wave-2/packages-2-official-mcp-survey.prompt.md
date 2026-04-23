# Ecosystem Wave 2: Official MCP Surface Survey

You are handling one workstream inside a larger Codex Cloud fanout for this repository.

Assume you are operating as a principal engineer with full autonomy to investigate this workstream.
You may inspect the repo deeply, run tests or benchmarks, prototype code, edit files, and use web or doc research when that materially improves the result.

## Objective

Survey the strongest official or de facto MCP servers that could back future ecosystem packages, and recommend which ones are good fits for this repo's package model.

## Why this workstream exists

This repo is intentionally MCP-first for many partner integrations. The scaling question is whether the underlying MCP server story is solid enough to support more packages without building a lot of bespoke SDK adapters. We need a grounded view of which partner surfaces already have credible MCP servers, what their auth/runtime story looks like, and whether they seem stable enough to package.

## Mode

- research
- recommendation only

Compare 2-3 credible directions where appropriate rather than forcing a single narrative.

## Operating assumptions

- Investigate like a principal engineer.
- Use primary docs and official repos when possible.
- Focus on MCP servers that a Python ecosystem package can realistically wrap with good docs and CI.
- Be skeptical of brittle hosted-only or OAuth-heavy stories unless there is a strong payoff.

## Required execution checklist

- You MUST inspect the current repo package model and tests.
- You MUST research at least 6 external MCP-backed candidate surfaces.
- You MUST separate:
  - official MCP servers
  - credible third-party MCP servers
  - weak or unstable options
- You MUST recommend which MCP surfaces are good candidates for package wrappers and which should remain examples/docs.
- You MUST write down auth, local testability, and hosted-smoke feasibility for each serious candidate.

## Required repo context

Read at least these:

- `README.md`
- `GOVERNANCE.md`
- `catalog/integrations.toml`
- `packages/pydantic_ai_partner_mcp/pydantic_ai_partner_mcp/_capability.py`
- `templates/partner_mcp/package__capability.py.tmpl`
- `templates/partner_mcp/test_capability.py.tmpl`

Inspect any additional files needed.

## Deliverable

Write one repo-local output at:

`reports/fanout/2026-04-23-ecosystem-wave-2/official-mcp-survey.md`

## Constraints

- favor primary sources over commentary
- do not confuse popularity with suitability
- distinguish "MCP exists" from "package-worthy"
- call out auth/test friction explicitly

## Success criteria

- A usable survey that informs package selection.
- Explicit guidance on which candidate packages can be MCP-first with minimal custom code.
- Concrete notes on what can be verified automatically.

## Decision style

End with:

- `Recommendation: <label>`
- `Best MCP-backed package candidates: <ordered list>`
- `Examples-only candidates: <short list>`
- `Biggest ecosystem risks: <short list>`
- `What would change my mind: <specific evidence>`
