import sys
import os
import asyncio

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from mcp.server.fastmcp import FastMCP
from tools.search_verse import search_verse
from tools.get_verse import get_verse
from tools.get_passage import get_passage

mcp = FastMCP("ScriptureInsight")

# Register our imported tools!
mcp.tool()(search_verse)
mcp.tool()(get_verse)
mcp.tool()(get_passage)

if __name__ == "__main__":
    mcp.run(transport='stdio')