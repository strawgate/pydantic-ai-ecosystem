# Ecosystem Wave 2: Package Roadmap And Priority

You are handling one workstream inside a larger Codex Cloud fanout for this repository.

Assume you are operating as a principal engineer with full autonomy to investigate this workstream.
You may inspect the repo deeply, run tests or benchmarks, prototype code, edit files, and use web or doc research when that materially improves the result.
Do not stop at a shallow summary if the right answer requires code inspection, experiments, or comparison of multiple approaches.

## Reality model

Assume you can rely on only:

- the committed repository state on the launched branch
- this prompt text

Assume you cannot rely on:

- any local branch, worktree, or uncommitted file from the person who launched this task
- hidden thread context from prior tasks
- repo-local fanout artifacts unless they are committed on the launched branch

## Objective

Produce a concrete recommendation for the next 5 partner or ecosystem packages this repo should build after the current first wave.

## Why this workstream exists

The repo now has a real MCP-first package base, stronger local MCP tests, a real LocalStack smoke test, and a real Playwright MCP smoke test. The next question is not "what is popular in abstract?" but "what should we build next that is both strategically valuable and realistically testable in CI without human setup?"

## Mode

- research
- recommendation only

Choose the single best ranked roadmap after investigation, but compare at least two plausible ranking approaches before deciding.

## Operating assumptions

- You are expected to investigate this like a principal engineer, not merely summarize nearby files.
- Use repo inspection, docs, tests, and web research as needed to produce a grounded result.
- Favor packages that can be verified automatically over packages that only sound exciting.
- Distinguish partner packages from generic MCP utility packages.
- Spend at least 10 minutes doing real investigation before finalizing unless tooling blocks you.
- Do not stop once you have one plausible ranking; keep working until the remaining new findings are likely low-value noise.

## Required execution checklist

- You MUST read the repo context files listed below before making recommendations.
- You MUST inspect the current package set and test shape.
- You MUST compare at least 8 candidate integrations, not just 3-4.
- You MUST end with a ranked top 5 and a separate watchlist.
- You MUST explain why each top-5 choice is buildable now.
- You MUST include expected test strategy and likely blocker per candidate.
- After completing the required work, use your judgment to explore adjacent options only if they materially improve the decision quality.

## Required repo context

Read at least these:

- `README.md`
- `GOVERNANCE.md`
- `catalog/integrations.toml`
- `packages/pydantic_ai_partner_mcp/README.md`
- `packages/pydantic_ai_localstack/README.md`
- `packages/pydantic_ai_playwright/README.md`
- `tests/pydantic_ai_localstack/test_localstack_capability.py`
- `tests/pydantic_ai_playwright/test_playwright_capability.py`

Inspect any additional files needed to make a grounded recommendation.

## Deliverable

Write one repo-local output at:

`reports/fanout/2026-04-23-ecosystem-wave-2/package-roadmap.md`

## Constraints

- ground everything in the actual repo
- optimize for testability, strategic fit, and clear capability value
- do not recommend packages that are basically just `MCP(url=...)` unless you can justify the package with actual UX or safety value
- separate "should be an example" from "should be a package"

## Success criteria

- A ranked next-wave package plan that a maintainer could plausibly execute.
- Clear reasoning about why these packages belong in the repo rather than docs/examples only.
- Enough detail to choose the next 2-3 packages immediately.

## Decision style

End with:

- `Recommendation: <label>`
- `Top 5: <ordered list>`
- `Primary rationale: <1-3 bullets>`
- `Watchlist: <short list>`
- `What would change my mind: <specific evidence>`
