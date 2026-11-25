# Prompt log – HW3 (L06: gmail-calendar MCP server)

Every prompt used in this assignment, in order, with what the agent did and the result.
Agent: **Claude Code** (Opus). Personal details (email address, Windows user name, private paths,
event links, contents of real emails) are replaced with placeholders such as
`C:\path\to\private-folder` and `<my-email>`.

There are two kinds of prompts here:
- **A – our instructions to the coding agent** (the Claude Code session that built the project).
  We wrote them in Hebrew; an English translation is given under each one.
- **B – the lesson prompts** (English, from the L06 deck).
  - Steps 2–7, 12 and 14 are the deck's build/test instructions. The coding agent carried them out
    **directly as part of brief A1** (it did the same work in the same session); they were not pasted
    one by one. The prompt text is kept here because it is what the work was measured against.
  - Steps 8–11 and 13 were **sent literally** as new agent runs: `claude -p "<prompt>"` in the HW3 folder,
    with the agent allowed **only the six gmail-calendar MCP tools**
    (`--allowedTools mcp__gmail-calendar__…`), so it could not answer by writing code.

---

## A1 – the assignment brief (Hebrew, to the coding agent)
> השיעור אנחנו לומדים MCP. פתחתי למשימה שקיבלנו תיקיה חדשה C:\biu01\LO7 בו נמצאת גם מצגת השיעור המלאה.
> תעבור על המצגת המלאה, תיקח את כל המשימות ומה שהמרצה ביקש בה ותבצע את המטלה בפרויקט החדש שפתחתי ב-GitHub
> https://github.com/greenlivnat/HW3.
> המטלה הראשונה, כבר הוצאתי לך:
> ```
> ① Build an MCP server in Python, named "gmail-calendar".
>    Use FastMCP, run it with uv, stdio transport.
> ② Reuse the Google client and token.json from last week.
>    Read the folder from GOOGLE_PRIVATE_DIR. Never copy them.
> ③ Expose exactly these tools, each with a clear description:
>    search_emails, read_email, create_draft,
>    list_events, find_free_slots, create_event
> ④ NO tool that sends or deletes. Time zone Asia/Jerusalem.
>    Add a .gitignore for token.json and client_secret*.json.
> ```

*English:* "This lesson is about MCP. I opened a new folder for the assignment, C:\biu01\LO7, which also
contains the full lesson deck. Go through the whole deck, take every task the lecturer asked for, and do
the assignment in the new GitHub project HW3. The first task, already extracted: (the brief above)."

**What the agent did:** extracted the text of the deck (14 steps + appendices), made a plan from it,
connected the folder to the HW3 repository.

## A2 – document your own work (mid-task)
> שים לב שאתה מכין reflection.md ושאתה עוקב אחרי העבודה של עצמך ומתעד אותה

*English:* "Make sure you prepare reflection.md, track your own work and document it."
**Result:** a work log (including every error and fix) was kept and written into
[reflection.md](reflection.md#work-log-what-the-agent-did-including-what-went-wrong).

## A3 – privacy (mid-task)
> שים לב גם שאתה לא מפרסם בגיט את הסיסמא שלי לחשבון GMAIL ולהסתיר פרטים אישיים

*English:* "Make sure you don't publish my Gmail password to Git, and hide personal details."
**Result:** the Gmail password is never used (the server only uses the OAuth token from the private
folder). Before each commit the staged files were scanned for the email address, user name, client
secret, token, event links and real email contents. `logs/`, `.agents/` and the slides are git-ignored.
Rules were added to [CLAUDE.md](CLAUDE.md).

## A4 – screenshots
> הנה צילומי המסך, תוסיף אותם ל-GIT

*English:* "Here are the screenshots, add them to Git."
**Result:** three screenshots added to `screenshots/`; two areas were blacked out first
(the Windows user name in a path, and an unrelated private email draft).

## A5 – this file
> אל תשכח לייצר לי גם תיעוד פרומטים מלא ב-GIT

*English:* "Don't forget to also create full prompt documentation in Git." → this file.

---

## B – lesson prompts (deck steps)

### Step 2 – check the working folder
> In one sentence: which folder are you working in, and is it empty?

Result: the agent worked in the HW3 folder (it held only the deck and the repo's README).

### Step 3 – check the keys from L05 (without opening them)
> Check that the folder `C:\path\to\private-folder` contains a Google client file (client_secret*.json)
> and a token.json file. Only tell me whether each file exists and its date.
> Do NOT print the contents of these files.

Result: both files exist (from last week). Their contents were not printed.

### Step 4 – build the server (the main prompt)
> Build an MCP server in Python in the current folder, named "gmail-calendar". Use the official MCP
> Python SDK (FastMCP), run it with uv, and use the stdio transport.
> It must reuse the Google client and token.json from last week. They are in the private folder
> `C:\path\to\private-folder`; read that path from the environment variable GOOGLE_PRIVATE_DIR.
> Never copy these files into this project, never print secrets, and never open a browser from the server.
> Expose exactly these tools, each with a short, clear English description:
> 1. search_emails(query, max_results)
> 2. read_email(message_id)
> 3. create_draft(to, subject, body) - a DRAFT only
> 4. list_events(days_ahead)
> 5. find_free_slots(date, duration_minutes)
> 6. create_event(title, start, end, description)
>
> There must be NO tool that sends or deletes anything. Time zone: Asia/Jerusalem. Keep each Python
> file under 150 lines. Add a .gitignore for token.json, client_secret*.json, credentials.json and .env.
> Write a README.md that explains how to run it.

Result: `server.py` (130 lines), `google_auth.py` (51), `pyproject.toml`, `.gitignore`, `README.md`.
**Problem:** the newest `mcp` package is 2.x, where FastMCP was renamed, so the server crashed on
import. **Fix:** pinned `mcp[cli]<2`.

### Step 5 – show what was built
> Show me the file tree of this folder. Then show a table of the tools in server.py: name, one-line
> description, and which Google API call each tool uses. Confirm that no tool sends or deletes
> anything, and show me the content of .gitignore.

Result: the table in [README.md](README.md#tools) – 6 tools, no send, no delete.

### Step 6 – self-test before connecting
> Write and run a small test script, test_server.py, that starts the server, asks it for its list of
> tools, and calls list_events with days_ahead=1. Set GOOGLE_PRIVATE_DIR=`C:\path\to\private-folder`
> for the test. Show me the output.

Result: `tools/list` → exactly the 6 tools; `tools/call list_events(1)` → Google answered; no auth error.

### Step 7 – register the server in Claude Code
> Register this server in Claude Code with "claude mcp add": local scope, name "gmail-calendar",
> stdio transport, the environment variable GOOGLE_PRIVATE_DIR=`C:\path\to\private-folder`, and the
> command "uv run --directory <this folder> server.py". Then tell me exactly what to do next.

Result: `✔ Connected`, 6 tools (see [screenshot](screenshots/01_mcp_connected.png)), after three
PowerShell fixes: quote `'--'`, put the name before `--env`, use the full path to `uv.exe`.

### Step 8 – first question (read-only)
> What do I have in my calendar tomorrow?

Tool used: `list_events`. Answer: nothing scheduled tomorrow; one test event today.

### Step 9 – the task (same as L05)
> Write a Gmail draft to myself with the subject "L06 test" and add a calendar event for today,
> 4 hours from now, called "MCP works".

Tools used: `create_draft` → draft **L06 test** in Drafts (not sent); `create_event` → **MCP works**
20:04–21:04 (request made at 16:04, Israel time). No new Python file was written.
See [Drafts](screenshots/02_gmail_drafts.png) and [Calendar](screenshots/03_calendar_events.png).

### Step 10 – a new request, same server
> Find a free hour tomorrow between 09:00 and 17:00 and add an event called "Study group" there.

Tools used: `find_free_slots` → `create_event`. Result: "Study group" tomorrow 09:00–10:00.

### Step 11 – test the boundary
> Great. Now send the "L06 test" draft.

> Delete the "Study group" event.

Result: both refused – the server has no send or delete tool. The draft stayed in Drafts, the event
stayed in the calendar. Note: the agent also tried other Google connectors installed in Claude Code;
only the permission prompt stopped it (see reflection, work log item 9).

### Step 13 ⭐ – meeting coordinator
> Act as my meeting coordinator. Find the latest meeting request in my email. Check my calendar for
> that time. If I am free, create the event and prepare a reply draft confirming it. If I am busy, do
> not create an event; prepare a reply draft that suggests two free times. Never send anything.
> Show me what you did, step by step.

Tools used: `search_emails` → `read_email` → `list_events` / `find_free_slots` → `create_draft`.
Result: the newest meeting request was a real one that was already in the calendar, so no event was
created; only a reply **draft** was saved and nothing was sent. Lesson: prepare a dedicated test email
for this step (details intentionally not published).

### Step 14 – reflection and README
> Create reflection.md with four empty sections: "What did we ask the agent?", "How did we check that
> the result is correct?", "Which tool did we leave out, and why?", "L05 vs L06: what changed?".
> Also add to README.md the list of prompts we used today. Then commit.

Result: [reflection.md](reflection.md) (answered and documented, see A2), prompt list in README,
and this full log.

### Step 12 – Git without secrets
> Initialize a git repository in this folder. Before the first commit, show me git status and confirm
> that no token.json, client_secret*.json or .env file will be committed. Then commit with the message
> "L06 gmail-calendar MCP server".

Result: `git status` showed only code and docs; commit `L06 gmail-calendar MCP server` pushed to HW3.
