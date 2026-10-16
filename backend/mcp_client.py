"""Local stdio MCP bridge; no public server or arbitrary file access."""
from contextlib import asynccontextmanager
import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def connect():
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / 'mcp_server.py')], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


def unpack(result) -> dict:
    if result.isError:
        raise ValueError('MCP tool rejected the request.')
    if result.structuredContent:
        return result.structuredContent
    for item in result.content:
        if item.type == 'text':
            return json.loads(item.text)
    raise ValueError('MCP tool returned no structured result.')


async def _call(name: str, arguments: dict) -> dict:
    async with connect() as session:
        return unpack(await session.call_tool(name, arguments))


def call_tool(name: str, arguments: dict) -> dict:
    return asyncio.run(asyncio.wait_for(_call(name, arguments), timeout=30))
