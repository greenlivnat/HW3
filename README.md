# HW3 – `gmail-calendar` MCP server

An MCP server in Python (FastMCP, run with **uv**, **stdio** transport) that gives an AI agent
(Claude Code, agy, Codex…) six tools for Gmail and Google Calendar.
It is the L05 exercise (draft + event) done again — this time the agent picks the tools itself.

## Tools

| Tool | What it does | Google API call |
|---|---|---|
| `search_emails(query, max_results)` | Search Gmail (Gmail search syntax), read-only | `gmail users.messages.list` + `get` (metadata) |
| `read_email(message_id)` | Headers + plain-text body of one email, read-only | `gmail users.messages.get` |
| `create_draft(to, subject, body)` | Creates a **draft only** – never sends | `gmail users.drafts.create` |
| `list_events(days_ahead)` | Events from now until the end of day N, read-only | `calendar events.list` |
| `find_free_slots(date, duration_minutes)` | Free slots on one day (default 09:00–17:00), read-only | `calendar freebusy.query` |
| `create_event(title, start, end, description)` | Creates one event – cannot edit/delete | `calendar events.insert` |

**Left out on purpose:** sending email (`users.messages.send`, `drafts.send`) and deleting
anything (emails or events). The agent prepares, the human sends/deletes.
Time zone everywhere: **Asia/Jerusalem**.

## Secrets – never in this repo
The server reuses last week's OAuth client and `token.json` (scopes `gmail.modify`, `calendar`).
They stay in a private folder outside the project; the server only reads the path from the
environment variable **`GOOGLE_PRIVATE_DIR`** (a folder, not a file). The server never opens a
browser: if the token is missing/invalid it returns a clear error – run last week's program once
to create a new `token.json`. `.gitignore` blocks `token.json`, `client_secret*.json`,
`credentials.json`, `.env`.

## Run
```powershell
uv sync
$env:GOOGLE_PRIVATE_DIR = "C:\path\to\private-folder"
uv run test_server.py      # self-test: lists the 6 tools and calls list_events(1)
```

## Connect to an agent
**Claude Code** (local scope – stored in `~/.claude.json`, not in this repo):
```powershell
claude mcp add gmail-calendar --scope local --transport stdio --env GOOGLE_PRIVATE_DIR=C:\path\to\private-folder '--' uv run --directory C:\path\to\HW3 server.py
```
Then restart `claude` and type `/mcp` → `gmail-calendar ✔ connected · 6 tools`.

Notes from doing it on Windows/PowerShell:
- put the server **name before** `--env` (otherwise `--env` swallows the name);
- quote the separator as `'--'` (PowerShell eats a bare `--`);
- if `/mcp` shows *failed* and `uv` was installed recently, use the full path to `uv.exe`.

**agy (Antigravity)** – `.agents/mcp_config.json` (kept out of Git because it holds a local path):
```json
{ "mcpServers": { "gmail-calendar": {
    "command": "uv",
    "args": ["run", "--directory", "C:\\path\\to\\HW3", "server.py"],
    "env": { "GOOGLE_PRIVATE_DIR": "C:\\path\\to\\private-folder" } } } }
```

## Prompts we used (in English, as required)
1. Step 4 – build: *Build an MCP server in Python in the current folder, named "gmail-calendar".
   Use the official MCP Python SDK (FastMCP), run it with uv, and use the stdio transport … Expose
   exactly these tools … There must be NO tool that sends or deletes anything. Time zone:
   Asia/Jerusalem …* (full text in the lesson deck, step 4)
2. Step 6 – self-test: *Write and run a small test script, test_server.py, that starts the server,
   asks it for its list of tools, and calls list_events with days_ahead=1.*
3. Step 7 – register: *Register this server in Claude Code with "claude mcp add": local scope,
   name "gmail-calendar", stdio transport, GOOGLE_PRIVATE_DIR, command "uv run --directory <folder> server.py".*
4. Step 8: *What do I have in my calendar tomorrow?*
5. Step 9: *Write a Gmail draft to myself with the subject "L06 test" and add a calendar event for
   today, 4 hours from now, called "MCP works".*
6. Step 10: *Find a free hour tomorrow between 09:00 and 17:00 and add an event called "Study group" there.*
7. Step 11: *Great. Now send the "L06 test" draft.* / *Delete the "Study group" event.*
8. Step 13 ⭐: *Act as my meeting coordinator. Find the latest meeting request in my email … Never send anything.*

**Full prompt log** – every prompt (ours to the coding agent, and the lesson prompts), in order,
with what the agent did and the result: [PROMPTS.md](PROMPTS.md).
The checks are summarised in [reflection.md](reflection.md).

## Screenshots
Personal details (Windows user name in a path, one unrelated private email draft) are blacked out.

| `/mcp` – server connected | Step 9 result – Gmail Drafts | Step 9 result – Calendar |
|---|---|---|
| ![/mcp shows gmail-calendar connected with 6 tools](screenshots/01_mcp_connected.png) | ![Draft "L06 test" in Gmail Drafts, not sent](screenshots/02_gmail_drafts.png) | ![Event "MCP works" 20:04–21:04, four hours after the request](screenshots/03_calendar_events.png) |

## Files
`server.py` (the 6 tools) · `google_auth.py` (loads the token) · `test_server.py` (self-test) ·
`pyproject.toml` / `uv.lock` (dependencies: `mcp[cli]<2`, Google API client, `tzdata`) ·
`reflection.md` · `.gitignore`
