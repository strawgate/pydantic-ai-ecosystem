from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    'Pydantic AI Ecosystem Partner Test Server',
    instructions='Use the test partner tools for workspace search and document reads.',
)


@mcp.tool()
async def search_workspace(query: str) -> dict[str, object]:
    """Search the test workspace for matching documents."""
    return {
        'query': query,
        'items': ['Alpha Doc', 'Beta Doc'],
        'count': 2,
    }


@mcp.tool()
async def read_document(document_id: str) -> str:
    """Read a document from the test workspace."""
    return f'Document {document_id}: Example content.'


if __name__ == '__main__':
    mcp.run()
