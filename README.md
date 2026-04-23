# `pydantic-ai-ecosystem`

This directory is a standalone implementation repo for ecosystem capability packages.

The design goals are:

- shared development tooling at the repo root
- separate runtime dependencies per package
- independent package publishing
- easy CI fan-out by changed package

The root `pyproject.toml` owns:

- the `uv` workspace
- shared developer tools
- shared lint, typecheck, and pytest configuration
- repo-level utility scripts and templates

Each package `pyproject.toml` owns:

- distribution metadata
- runtime dependencies
- optional extras
- package-local entry points or scripts if needed

## Layout

```text
pydantic-ai-ecosystem/
├── README.md
├── pyproject.toml
├── .github/
│   └── workflows/
│       └── ci.yml
└── packages/
    ├── pydantic_ai_github/
    │   └── pyproject.toml
    ├── pydantic_ai_localstack/
    │   └── pyproject.toml
    ├── pydantic_ai_logfire/
    │   └── pyproject.toml
    ├── pydantic_ai_notion/
    │   └── pyproject.toml
    ├── pydantic_ai_partner_mcp/
    │   └── pyproject.toml
    ├── pydantic_ai_playwright/
    │   └── pyproject.toml
    ├── pydantic_ai_slack/
    │   └── pyproject.toml
    └── pydantic_ai_aws/
    │   └── pyproject.toml
├── scripts/
│   ├── ci_matrix.py
│   ├── integration_priority.py
│   └── scaffold_partner_package.py
└── templates/
    └── partner_mcp/
        └── *.tmpl
```

## Why This Split

Partner capabilities should not share one runtime package because they have different dependencies and should release independently.

Examples:

- `pydantic-ai-aws` can depend on `boto3` and AWS-specific test helpers
- `pydantic-ai-localstack` can depend on MCP support and LocalStack-specific integration tooling
- `pydantic-ai-github` can depend on GitHub-oriented HTTP clients or MCP integrations
- `pydantic-ai-logfire` can depend on Logfire directly
- `pydantic-ai-partner-mcp` can provide shared MCP plumbing for lightweight partner packages
- `pydantic-ai-playwright` can focus on browser automation defaults without dragging browser setup into unrelated packages
- `pydantic-ai-slack` can depend on the Slack SDK

That keeps install surfaces narrow and avoids dragging infrastructure-specific dependencies into unrelated packages.

## CI Model

The included workflow is intentionally simple:

- always run shared lint, typecheck, and docs checks
- detect changed packages at the package-directory level
- run package tests only for affected packages
- run heavier integration jobs separately when needed

Automated verification also drives package priority. See [GOVERNANCE.md](GOVERNANCE.md) and the
machine-readable candidate catalog in [catalog/integrations.toml](catalog/integrations.toml).

## Publish Model

Each package should publish to PyPI independently:

- `pydantic-ai-aws`
- `pydantic-ai-github`
- `pydantic-ai-localstack`
- `pydantic-ai-logfire`
- `pydantic-ai-partner-mcp`
- `pydantic-ai-playwright`
- `pydantic-ai-slack`

The monorepo exists for shared tooling, docs, and release automation, not because the packages should move in lockstep.

## Current Focus

The first wave of packages is intentionally narrow:

- `pydantic-ai-aws`: generic AWS-facing integrations, likely centered on the AWS API MCP server
- `pydantic-ai-github`: GitHub-facing capability scaffolding for engineering agents
- `pydantic-ai-localstack`: the LocalStack-first capability package that should feel native in Pydantic AI
- `pydantic-ai-logfire`: observability and tracing capability scaffolding
- `pydantic-ai-notion`: generated from the shared partner template as the first fan-out-safe scaffold
- `pydantic-ai-partner-mcp`: shared base for MCP-first partner packages
- `pydantic-ai-playwright`: a highly testable browser-automation capability package
- `pydantic-ai-slack`: Slack-facing capability scaffolding for collaboration workflows

If this repo succeeds, `pydantic-ai-localstack` should become the clearest path for getting LocalStack recognized in the broader Pydantic AI ecosystem and, eventually, a candidate for Pydantic AI Harness.

The next implementation wave should be driven by automated-testability first, not by brand recognition
alone. A ranked report is available via:

```bash
uv run python -m scripts.integration_priority --top 10
```

New MCP-first partner packages should be scaffolded instead of copied by hand:

```bash
uv run python -m scripts.scaffold_partner_package \
  --slug notion \
  --display-name Notion \
  --partner-instruction "Prefer updating existing pages and databases before creating new ones." \
  --agent-instructions "Help the user work with Notion content and workspace knowledge."
```
