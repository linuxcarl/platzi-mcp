
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def sum(a:int, b:int) -> int:
    """
    Returns the sum of two integers.
    """
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
        Get a personalized greeting
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()