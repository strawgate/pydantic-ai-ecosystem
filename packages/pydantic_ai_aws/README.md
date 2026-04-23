# Pydantic AI AWS

Implementation package for generic AWS capability integrations.

Initial direction:

- `AWSAPIMCPCapability` as the primary surface
- AWS API MCP server as the default backend
- explicit environment targeting rather than silent fallback

This package should stay generic. It is not the primary LocalStack story.
