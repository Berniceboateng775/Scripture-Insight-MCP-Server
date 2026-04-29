import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripture-mcp')))

from services.search_service import search_verses

results = search_verses("love and sacrifice")

print(results)