import datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP

mcp = FastMCP("mvfm's mcp server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b


@mcp.tool
def now() -> datetime.datetime:
    """Returns the current date and time"""
    return datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))


if __name__ == "__main__":
    mcp.run()
