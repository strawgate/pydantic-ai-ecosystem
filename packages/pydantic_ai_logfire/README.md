# Pydantic AI Logfire

Implementation package for Logfire capability integrations.

Initial direction:

- `LogfireCapability` as the primary surface
- trace-oriented configuration that can be loaded from specs
- a future path to hooks, spans, and evaluation metadata without touching agent code

This package should become the observability partner capability for Pydantic AI agents.
