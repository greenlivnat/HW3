# Reflection – L06: the L05 exercise through an MCP server

> Personal details (email address, Windows user name, event links, contents of real emails)
> were removed on purpose. The raw run logs stay on the local computer only (`logs/`, ignored by Git).

## What did we ask the agent?
- To **build** an MCP server `gmail-calendar` (FastMCP, uv, stdio) with exactly six tools –
  `search_emails`, `read_email`, `create_draft`, `list_events`, `find_free_slots`, `create_event` –
  reusing last week's OAuth client and `token.json` from the private folder (`GOOGLE_PRIVATE_DIR`),
  with **no** tool that sends or deletes, time zone Asia/Jerusalem, a `.gitignore` for secrets,
  and every Python file under 150 lines.
- To **test** it (`test_server.py`), **register** it in Claude Code (`claude mcp add`, local scope),
  and then to use it with free-language requests only (steps 8–11, 13). The exact prompts are in
  [README.md](README.md#prompts-we-used-in-english-as-required).

## How did we check that the result is correct?
| Check | Result |
|---|---|
| `test_server.py`: tools/list | exactly the 6 tools, each with an English description; no `send`/`delete` in any name |
| `test_server.py`: tools/call `list_events(1)` | Google answered (no auth error) – returned the L05 test event |
| `find_free_slots` on a day that looked empty | returned nothing → checked the raw free/busy answer: a real event covered the whole day, so the tool was right |
| `claude mcp get gmail-calendar` | `✔ Connected` (after a fix, see work log) |
| Step 8 – "What do I have tomorrow?" | answered via `list_events`, matched the calendar |
| Step 9 – draft + event | `create_draft` → draft **L06 test** in Drafts (not sent); `create_event` → **MCP works** exactly 4 h after the request time, Israel time; **no new .py file** was written |
| Step 10 – "Study group" | `find_free_slots` → first free hour tomorrow 09:00–10:00 → `create_event` |
| Step 11 – "send" / "delete" | refused both: the server has no such tools; the draft stayed in Drafts and the event stayed in the calendar |

Screenshots: [`/mcp` connected](screenshots/01_mcp_connected.png) ·
[draft "L06 test" in Drafts](screenshots/02_gmail_drafts.png) ·
[event "MCP works" at 20:04, request made at 16:04](screenshots/03_calendar_events.png).

The agent in steps 8–13 ran as `claude -p` and was **allowed only the six gmail-calendar tools**
(no Bash/Python), so it could not "solve" a request by writing a script.

## Which tool did we leave out, and why?
**Sending email** (`users.messages.send` / `drafts.send`) and **deleting** anything.
The agent reads email content, and an email can contain hidden instructions (prompt injection,
e.g. "forward all emails to …"). Without a send/forward/delete tool there is nothing to execute –
the worst case is an unwanted *draft* or an extra event, which a human sees and can remove.
The human stays in the loop: the agent prepares, the person presses **Send**.

## L05 vs L06: what changed?
| | L05 – `main.py` | L06 – MCP server |
|---|---|---|
| New request | new prompt + new program | same server, one sentence |
| Who chooses the steps | the code, fixed order | the model, from the tool menu |
| "Is the calendar busy?" | not checked | `find_free_slots` |
| Who can use it | this program only | any MCP host (Claude Code, agy, Codex…) |
| Safety boundary | what the code does | which tools exist (no send/delete) |
| Cost | no tokens | tool descriptions are sent to the model on every turn |
| Secrets | private folder | the **same** private folder – nothing new, nothing copied |

---

## Work log (what the agent did, including what went wrong)
1. Read the full lesson deck (`L06-MCP-Gmail-Calendar_slides-v03.html`, 14 steps + appendices)
   and extracted the tasks. The deck itself is the lecturer's material and is **not** committed.
2. Connected the local folder to the GitHub repo `HW3`.
3. Created the uv project and installed `mcp[cli]` + Google libraries.
4. **Problem:** the newest `mcp` package is **2.x**, where `FastMCP` was renamed (`MCPServer`), so
   the server crashed on import and the self-test reported "Connection closed".
   **Fix:** pinned `mcp[cli]<2` (the assignment asks for FastMCP). Self-test passed.
5. Wrote `server.py` (130 lines), `google_auth.py` (51), `test_server.py` (38). Logging goes to
   stderr only – stdout is the MCP pipe. The server never opens a browser.
6. Suspected a bug in `find_free_slots` (an empty day returned no slots); inspected the raw
   `freebusy` answer – a real all-day-long event – so no change was needed.
7. Registration problems in PowerShell, fixed one by one:
   bare `--` was swallowed (→ `'--'`); `--env` swallowed the server name (→ name first);
   `/mcp` status *Failed to connect* because `uv` was installed after Claude Code started
   (→ full path to `uv.exe`). Final status: **Connected**.
8. Ran steps 8, 9, 10, 11 through Claude Code with only the MCP tools allowed – all as expected.
9. **Lesson from step 11:** besides our server, the host (Claude Code) had *other* Google
   connectors installed, and the agent tried them to delete the event; only the permission prompt
   stopped it. The tool boundary of our server is real, but the host's other connectors and the
   permission prompts are part of the safety boundary too – read every approval request.
10. **Lesson from step 13 (⭐ meeting coordinator):** we did not prepare a dedicated test email, so
    the agent picked the newest *real* meeting email in the inbox. It behaved correctly – it saw the
    meeting was already in the calendar (twice), did **not** create a duplicate, and only saved a
    reply **draft** (nothing sent) – but next time run this step on a test email sent for it.
11. Before committing: checked `git status` and the file contents for secrets and personal details
    (email address, user name, private-folder path, event links); none are in the repo.
    `.gitignore` also excludes `logs/`, `.agents/` and the slides file.
12. Added the three screenshots. Before committing them, checked each image for personal data and
    blacked out two areas: the Windows user name inside the `.claude.json` path (`/mcp` screen) and
    the step-13 reply draft to a real recruiter (Gmail Drafts screen). The calendar screen was clean.
