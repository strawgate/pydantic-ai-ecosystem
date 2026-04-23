# Ecosystem Wave 2: Existing Packages Through User Goals

You are handling one workstream inside a larger Codex Cloud fanout for this repository.

Assume you are operating as a principal engineer with full autonomy to investigate this workstream.
You may inspect the repo deeply, run tests, prototype code, edit files, and use web or doc research when that materially improves the result.

## Objective

Improve the existing partner packages by evaluating them the way a real user would: "I want to accomplish a goal with GitHub, Logfire, Slack, or Notion," not "I want a thin capability wrapper."

## Why this workstream exists

The current packages are structurally stronger now, with real local MCP tests, but some of them may still be too package-centric rather than goal-centric. We need to know where docs, defaults, examples, or capability instructions are missing from a user point of view.

## Mode

- implementation
- investigate + implement + test

Compare multiple plausible improvements, but end by making the highest-value changes you can justify.

## Operating assumptions

- Investigate like a principal engineer and product-minded maintainer.
- Evaluate the package surfaces as if you were a user trying to solve a task.
- Favor improvements that make the packages easier to understand and adopt.
- Strengthen docs, examples, tests, or ergonomics where that meaningfully helps.

## Required execution checklist

- You MUST inspect GitHub, Logfire, Slack, and Notion packages and their tests.
- You MUST define at least one realistic user goal per package.
- You MUST identify where the current docs or ergonomics fall short for those goals.
- You MUST implement the highest-value improvements you find, not just write a memo.
- You MUST run relevant tests/checks for changed files.

## Required repo context

Read at least these:

- `README.md`
- `packages/pydantic_ai_github/README.md`
- `packages/pydantic_ai_logfire/README.md`
- `packages/pydantic_ai_slack/README.md`
- `packages/pydantic_ai_notion/README.md`
- `tests/pydantic_ai_github/test_github_capability.py`
- `tests/pydantic_ai_logfire/test_logfire_capability.py`
- `tests/pydantic_ai_slack/test_slack_capability.py`
- `tests/pydantic_ai_notion/test_notion_capability.py`

## Deliverable

Write one repo-local output at:

`reports/fanout/2026-04-23-ecosystem-wave-2/existing-user-goals.md`

Also edit the repo where warranted and list changed files in the final note.

## Constraints

- keep changes coherent with the existing package model
- focus on user-facing clarity and adoption, not speculative abstractions
- prefer better docs/examples/defaults over adding unnecessary code

## Success criteria

- At least one meaningful repo improvement for current packages.
- Clear articulation of what a user is actually trying to do with each package.
- Better ergonomics or docs that a maintainer would plausibly keep.

## Decision style

End with:

- `Recommendation: <label>`
- `Main user-goal gaps: <short list>`
- `Changes made: <short list>`
- `What would change my mind: <specific evidence>`
