# Pydantic AI LocalStack

Implementation package for LocalStack capability integrations.

Initial direction:

- `LocalStackCapability` as the primary surface
- LocalStack-specific instructions and guardrails
- LocalStack MCP or AWS API MCP as an implementation detail

This package is the LocalStack-facing package users should actually adopt.

## Testing

The package should be verifiable without manual testing:

- fast unit tests for construction and spec support
- deterministic agent tests where needed
- an automated MCP smoke test that starts the real LocalStack MCP server and completes a handshake

The smoke test can be enabled with `PYDANTIC_AI_RUN_LOCALSTACK_MCP_TESTS=1`.
