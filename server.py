from fastmcp import FastMCP

mcp = FastMCP("mvfm's mcp server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b


if __name__ == "__main__":
    mcp.run()
