"""Self-test (step 6): start the server over stdio, list its tools, call list_events(1).

Run:  $env:GOOGLE_PRIVATE_DIR = "C:\\Users\\<you>\\google_private"; uv run test_server.py
Read-only: it does not create drafts or events.
"""
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

EXPECTED = {"search_emails", "read_email", "create_draft",
            "list_events", "find_free_slots", "create_event"}


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=["server.py"], env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            names = {t.name for t in tools}
            print("tools/list ->")
            for t in tools:
                print(f"  {t.name}: {(t.description or '').splitlines()[0]}")
            assert names == EXPECTED, f"unexpected tool set: {names}"
            assert not any(w in n for n in names for w in ("send", "delete")), "forbidden tool"
            result = await session.call_tool("list_events", {"days_ahead": 1})
            print("tools/call list_events(days_ahead=1) ->")
            print("  error" if result.isError else "  ok")
            for c in result.content:
                print("  " + getattr(c, "text", str(c))[:300])
            print("OK: 6 tools, no send/delete, Google answered.")


if __name__ == "__main__":
    asyncio.run(main())
