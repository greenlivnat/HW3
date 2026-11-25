# HW3 – gmail-calendar MCP server

Python MCP server (FastMCP from `mcp[cli]<2`, uv, stdio) with 6 tools for Gmail + Google Calendar.
See README.md for tools, run and registration instructions.

## Rules
- Secrets (`client_secret*.json`, `token.json`) live only in the folder named by `GOOGLE_PRIVATE_DIR`.
  Never copy them here, never print them, never commit them.
- Never commit personal details: email addresses, Windows user names, private paths, event links,
  contents of real emails. Use placeholders such as `C:\path\to\private-folder`.
- No tool may send email or delete anything. Time zone: Asia/Jerusalem.
- Never print to stdout in `server.py` (it is the MCP pipe).
- Keep each Python file under 150 lines. Keep README.md and reflection.md up to date.
