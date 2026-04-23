# Ecosystem Wave 2: Scaling Rules And Package Admission

You are handling one workstream inside a larger Codex Cloud fanout for this repository.

Assume you are operating as a principal engineer with full autonomy to investigate this workstream.
You may inspect the repo deeply, run tests, prototype code, edit files, and use web or doc research when that materially improves the result.

## Objective

Propose the package-admission, maturity-tier, and scaling rules this repo should adopt before it grows beyond the current first wave.

## Why this workstream exists

The repo now has enough real surface area that "just add more packages" would quickly create drift. We need a sharper operating model for what belongs here, what test bar each maturity tier needs, and when a package should stay a docs example instead of being promoted into the repo.

## Mode

- research
- investigate + implement + test

Choose the single best governance direction after comparing plausible alternatives. If the repo should change to reflect that direction, make the smallest high-value edit set and verify it.

## Operating assumptions

- Treat the repo as a real implementation repo, not a sketch.
- Compare this repo's current model against other ecosystems when helpful.
- Favor clarity and maintainability over elaborate process.
- If the existing governance docs are too vague, tighten them.

## Required execution checklist

- You MUST inspect the current governance, README, catalog, and scaffold story.
- You MUST identify at least 3 concrete failure modes if the repo scales without stronger rules.
- You MUST propose a maturity model that distinguishes real packages from scaffolds.
- You MUST either update repo docs/governance to reflect your recommendation or explain precisely why not.
- You MUST run relevant tests or checks if you change files.

## Required repo context

Read at least these:

- `README.md`
- `GOVERNANCE.md`
- `catalog/integrations.toml`
- `scripts/integration_priority.py`
- `scripts/scaffold_partner_package.py`
- `templates/partner_mcp/README.md.tmpl`
- `templates/partner_mcp/test_capability.py.tmpl`

## Deliverable

Write one repo-local output at:

`reports/fanout/2026-04-23-ecosystem-wave-2/scaling-rules.md`

If you edit repo docs or governance files, list those changes in the final note.

## Constraints

- stay grounded in this repo's current state
- avoid bureaucracy for its own sake
- separate admission rules, maturity rules, and CI requirements cleanly

## Success criteria

- A maintainable scaling model for the next wave.
- Clear admission rules for when to add packages.
- If docs are updated, they should make the repo more coherent for contributors.

## Decision style

End with:

- `Recommendation: <label>`
- `Primary rationale: <1-3 bullets>`
- `Key rule changes: <short list>`
- `What would change my mind: <specific evidence>`
