"""HornetFlow MCP server. Stdout is reserved for protocol messages."""
from mcp.server.fastmcp import FastMCP
from backend.validation import ROOT, check_appeal, lookup_student

mcp = FastMCP('HornetFlow', instructions='Synthetic student records and demo policy only. Never claim aid approval.')
mcp.tool()(lookup_student)
mcp.tool()(check_appeal)


@mcp.tool()
def get_appeal_policy() -> dict:
    """Read the synthetic demo appeal policy; not official university guidance."""
    return {'source': 'data/demo-policy.md', 'synthetic': True,
            'policy': (ROOT / 'data/demo-policy.md').read_text()}


@mcp.resource('hornetflow://policy')
def policy_resource() -> str:
    return (ROOT / 'data/demo-policy.md').read_text()


if __name__ == '__main__':
    mcp.run(transport='stdio')
