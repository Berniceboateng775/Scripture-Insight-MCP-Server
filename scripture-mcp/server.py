import sys
import os
import asyncio

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from mcp.server.fastmcp import FastMCP
from tools.search_verse import search_verse
from tools.get_verse import get_verse
from tools.get_passage import get_passage
from tools.cross_reference import get_cross_references
from tools.topic_lookup import get_topic_verses
from tools.original_language_lookup import original_language_lookup
from tools.character_profile import character_profile
from tools.timeline_event_lookup import timeline_event_lookup
from tools.summarize_passage import summarize_passage

mcp = FastMCP("ScriptureInsight")

# Register our imported tools!
mcp.tool()(search_verse)
mcp.tool()(get_verse)
mcp.tool()(get_passage)
mcp.tool()(get_cross_references)
mcp.tool()(get_topic_verses)
mcp.tool()(original_language_lookup)
mcp.tool()(character_profile)
mcp.tool()(timeline_event_lookup)
mcp.tool()(summarize_passage)

if __name__ == "__main__":
    mcp.run(transport='stdio')