from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SSE demo")


app = Starlette(
    routes = [
        Mount('/', app =mcp.sse_app())
    ]
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
