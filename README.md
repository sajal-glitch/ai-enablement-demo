# AI Enablement Demo — Phase 1 Sample Repository

This is the sample project used across both Phase 1 sessions. Every live demo
in the lesson plan maps to a specific file in this repo.

---

## Quick Setup

```bash
# 1. Clone / open the repo
cd ai-enablement-demo

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the API server
uvicorn app.main:app --reload

# 5. Open the interactive docs
# → http://127.0.0.1:8000/docs

# 6. Run tests
pytest tests/ -v --tb=short
```

---

## Demo Map — Every Module, Step by Step

---

### SESSION 1 / MODULE 1 — Claude Code: Five Interfaces

#### Demo A · Claude Chat — Refactor a Broken Function
**File:** `app/sales_processor.py`  
**Time:** ~10 minutes  
**Surface:** claude.ai browser tab

**Setup before class:**
- Open `app/sales_processor.py` in your editor so participants can see it on screen.
- Run the broken function to show it crash:
  ```bash
  python -c "
  from app.sales_processor import process_monthly_totals
  process_monthly_totals('data/sales_sample.csv')
  "
  ```
  It will raise a parsing error due to the messy dates in the CSV.

**The Demo:**

1. Open `claude.ai` in a browser tab.
2. Say out loud: *"Watch what happens when I use a bad prompt first."*
3. Type this **bad prompt** and send it:
   ```
   fix this code
   [paste process_monthly_totals function]
   ```
   Point out the generic, low-quality response — Claude makes assumptions.

4. Now send the **good prompt**:
   ```
   I have a Python function that reads a CSV of sales data and computes monthly
   totals. The function breaks if a row has missing values or the date column
   has inconsistent formats (e.g. "Jan 2024", "2024/01/15", "not-a-date").

   Here is the current code:
   [paste process_monthly_totals]

   Refactor this to:
   1. Handle missing revenue/units values gracefully (treat as 0)
   2. Normalize inconsistent date formats using pandas
   3. Add type hints to the function signature
   4. Add a Google-style docstring
   5. Return only the refactored function — no explanation needed
   ```
   
5. Show the quality difference live. Point out: type hints, docstring, error handling.

6. **Multi-turn follow-up** (shows conversational capability):
   ```
   Now add pytest unit tests for the refactored function. Cover:
   1. Happy path with a clean CSV
   2. CSV with missing revenue values
   3. CSV with unparseable dates
   4. CSV missing required columns
   Use pytest fixtures and tmp_path. Return only the test file.
   ```

**Teaching point:** *"Same task. 45 extra seconds to write a better prompt.
The output went from unusable to production-ready."*

---

#### Demo B · Claude Code Terminal — Add a Health Endpoint
**File:** `app/main.py`  
**Time:** ~10 minutes  
**Surface:** Terminal window

**Setup before class:**
- Have the terminal open in the project root.
- The API should be running in a separate terminal: `uvicorn app.main:app --reload`

**The Demo:**

1. In a new terminal, run:
   ```bash
   cd ai-enablement-demo
   claude
   ```
   Point out: *"Claude Code is now reading the project structure automatically."*

2. Type this prompt (do NOT press Enter yet — let participants read it):
   ```
   Add a GET /health endpoint to app/main.py that returns:
   - the application version (from app.__version__)
   - the current UTC timestamp in ISO format
   - a status field set to "ok"
   Return a JSON response. Add it after the imports, before the first route.
   ```

3. Press Enter. Show the diff Claude proposes.

4. Walk through the diff out loud: *"Before I accept this, I'm reviewing it.
   This is your responsibility — the AI drafts, you decide."*

5. Accept the changes.

6. In the API terminal, the server reloads automatically. Show:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
   Or open `http://127.0.0.1:8000/health` in the browser.

**Teaching point:** *"Claude Chat is for thinking. Claude Code is for doing.
Chat helps you plan; Code builds it in your actual repo."*

---

#### Demo C · Web → Artifact
**Surface:** claude.ai browser tab  
**Time:** ~5 minutes

1. In claude.ai, type:
   ```
   Generate a React component called SalesCard that shows:
   - A metric title (string prop)
   - A current value (number prop)
   - A percentage change vs last period (number prop)
   - A trend arrow: green up-arrow if positive, red down-arrow if negative
   Use Tailwind CSS classes only. Return only the component.
   ```

2. Point out the artifact rendering in the preview panel on the right.

3. Iterate live:
   ```
   Make the card background dark navy (#0F2044) and the percentage text gold
   (#F5A623) when positive.
   ```

4. Download/copy the component.

**Teaching point:** *"This is now a deliverable I can hand to someone,
embed in a dashboard, or iterate on further — all from a conversation."*

---

#### Guided Practice — Participants Do It Themselves
**Time:** ~5 minutes

Each participant:
1. **Terminal CLI:** Open a terminal in the sample repo → run `claude` → ask:
   *"Add a docstring to the process_monthly_totals function in app/sales_processor.py"*
   → Confirm the file is modified.

2. **IDE Extension:** Open the repo in VS Code → highlight `process_sales_data`
   in `app/sales_processor.py` → open the Claude chat panel → type `/explain`
   → Read the explanation.

3. **Web → Artifact:** Open claude.ai → ask Claude to generate a simple bar chart
   React component using the sales summary data shape.

---

### SESSION 1 / MODULE 2 — Data Privacy & IP Guardrails

No code demo. Facilitator runs the Scenario Walkthrough from the slide deck.
Files that appear in the scenarios:
- **Scenario A** — participants describe the schema of `app/models.py` instead of
  pasting real records (User model with email, name, etc.)
- **Scenario B** — `data/sales_sample.csv` contains sample rows they can
  use as synthetic data examples.

---

### SESSION 1 / MODULE 3 — Prompt Engineering

**File:** `app/sales_processor.py` (the `process_sales_data` function)

For the Bad vs. Good Prompt demo:
- **Bad prompt:** `"Write me a function to process data"`
- **Good prompt (exact text from lesson plan):**
  ```
  You are a senior data engineer.
  Write a Python function called process_sales_data that takes a pandas DataFrame
  with columns [date, region, revenue, units]. The function should:
  1) Validate that all required columns exist
  2) Convert date to datetime
  3) Add a 'quarter' column derived from the date
  4) Return the processed DataFrame
  Include type hints and a Google-style docstring. Return only the function.
  ```

The reference implementation is already in `app/sales_processor.py` so
participants can compare Claude's output to the expected result.

**Hands-on rewrite exercise:**
- Bad prompt: `"Help me with my API"`
- Participants rewrite using: Role + Context + Steps + Output Format
- Good answer example:
  ```
  You are a senior backend engineer specialising in FastAPI.
  I have a GET /users endpoint in app/main.py (FastAPI, SQLite, Python 3.11).
  The endpoint currently accepts any query parameters without validation.
  
  Do the following in order:
  1. Review the current /users route in app/main.py
  2. Add input validation for the 'region' parameter (must be one of:
     APAC, EMEA, NA, LATAM)
  3. Add a proper 422 error response if validation fails
  4. Return only the modified route function — not the full file
  ```

---

### SESSION 2 / MODULE 1 — Plan Mode & Context Distillation

#### Plan Mode Demo — Redis Caching
**File:** `app/cache.py`  
**Time:** ~10 minutes  
**Surface:** Terminal (Claude Code)

**Setup:** `app/cache.py` is intentionally left as stubs with `raise NotImplementedError`.
This makes the "before" state obvious.

**The Demo:**

1. Open Claude Code: `claude` in the terminal.
2. Type this prompt (read it aloud to participants before sending):
   ```
   Use plan mode. I need to add a caching layer to this API.
   We have a FastAPI service with 5 endpoints. I want to add Redis caching
   for the 3 read-heavy endpoints (/users, /orders, /sales/summary) with:
   - Configurable TTL per endpoint (defined in app/cache.py as CACHE_TTL dict)
   - Cache invalidation when data changes (POST /orders should clear order/sales cache)
   - A fallback: if Redis is down, the API should still work (query DB directly)
   
   Plan the implementation before writing any code.
   ```

3. Claude generates a structured plan. **Read it aloud with the class.**

4. Challenge assumptions out loud (model this behaviour for participants):
   - *"Why Redis over in-memory caching?"*
   - *"What happens if Redis goes down — does the whole API go down?"*
   - *"Which files get modified in what order?"*

5. Refine: *"Add the fallback strategy explicitly to the plan."*

6. Only after participants agree the plan is solid: *"Now implement step 1 only."*

**Teaching point:** *"The plan is where your expertise matters most.
You review it, catch wrong assumptions, and redirect BEFORE any code is written."*

---

#### Guided Practice — Input Validation Planning
**File:** `app/main.py` → `/users` endpoint  
**Time:** ~5 minutes

Each participant pairs up and uses plan mode:
```
Use plan mode. Plan the addition of input validation to the GET /users endpoint
in app/main.py. The endpoint currently accepts any query parameter without
checking if 'region' is a valid value. Plan:
1. The validation schema (which values are valid for 'region')
2. The error response format (status code, response body)
3. The test cases needed in tests/test_api.py
Do NOT write any code yet.
```

Pairs review each other's plans and give one piece of feedback.

---

### SESSION 2 / MODULE 2 — CLAUDE.md Exercise

**File:** `CLAUDE.md` (the partially completed template)  
**Time:** ~10 minutes

Participants open `CLAUDE.md` and fill in all `[FILL IN]` sections by
reading the source files.

**After filling it in — the verification test:**
1. Close all Claude Code sessions.
2. Open a new terminal → run `claude`
3. Ask: *"What testing framework does this project use, and where should test files go?"*

If the CLAUDE.md is correct, Claude's answer should reflect:
- pytest
- Files in `/tests/` mirroring `/app/` structure
- No mock.patch — use dependency injection

If Claude doesn't know, the CLAUDE.md is incomplete — participant fixes and retries.

---

### SESSION 2 / MODULE 3 — Agent Skills & Slash Commands

#### /review Command Demo
**File:** `tests/test_api.py`  
**Time:** ~5 minutes

1. Open Claude Code in the terminal.
2. Type: `/review tests/test_api.py`
3. Claude will flag: missing auth tests, no rate limit tests, no test for limit
   parameter bounds, etc.

**Teaching point:** *"This is a reusable skill. Every time you create a test file,
/review runs the same checklist. Consistent quality without repeating yourself."*

#### /eda Command Demo
**File:** `data/sales_sample.csv`  
**Time:** ~5 minutes

1. In Claude Code: `/eda data/sales_sample.csv`
2. Claude runs the full EDA: shape, types, missing values, outliers,
   distributions, correlations, key observations.
3. Point out the `not-a-date` row and missing revenue value — Claude catches them.

**Teaching point:** *"Before the /eda skill, someone was writing this report
manually for every new dataset. Now it runs in 10 seconds and follows the same
structure every time."*

---

### SESSION 2 / MODULE 4 — Parallel Worktrees

**Time:** ~10 minutes  
**No code changes needed** — pure Git demo.

```bash
# Terminal 1 (main branch — stay here)
cd ai-enablement-demo
git init          # if not already a git repo
git add .
git commit -m "initial commit"

# Create a feature branch and a worktree for it
git worktree add ../demo-feature-branch feature/add-caching

# Terminal 2 — open this in a SEPARATE terminal window
cd ../demo-feature-branch
claude
# → Prompt: "Implement the get_cache_client() function in app/cache.py
#   using redis-py. Use REDIS_URL env var for connection. Include the
#   Redis outage fallback."
```

**Back in Terminal 1** (simultaneously):
```bash
claude
# → Prompt: "Write a load test for GET /users using httpx.
#   Simulate 10 concurrent users, report average and p95 latency."
```

Show both terminals side by side. Both Claude Code sessions run at the same time.

**Teaching point:** *"One TL builds the cache implementation. The other writes
load tests. Same repo, different branches, fully parallel."*

---

### SESSION 2 / MODULE 5 — MCP Integration

No local code changes — this is an architecture explanation demo.

**Talking points while pointing at `app/database.py`:**

1. *"Right now, Claude helps with code that TALKS to the database.
   It doesn't query the database directly. That's the privacy boundary."*

2. *"With MCP, Claude would query the database through a secure server
   running in your infrastructure. Like this:"*
   - Draw: `Claude Code → MCP Client → MCP Server (your infra) → SQLite/Postgres`
   - *"Raw data never enters the conversation. Claude sends a query,
     gets back only the rows it needs."*

3. *"Where would this help in YOUR domain?"*
   - Ask participants to name 2–3 workflows where MCP would remove the
     need to paste data into prompts.
   - Common answers: EDA on production data, model validation against real
     outcomes, querying feature stores.

---

## Repository Structure

```
ai-enablement-demo/
├── CLAUDE.md                        ← Session 2 / M2 exercise target
├── README.md                        ← This file + full demo guide
├── requirements.txt
│
├── app/
│   ├── __init__.py                  ← App version string
│   ├── main.py                      ← FastAPI routes (S1/M1 terminal demo)
│   ├── models.py                    ← Pydantic models
│   ├── database.py                  ← SQLite + seed data
│   ├── cache.py                     ← Redis stub (S2/M1 plan mode demo)
│   ├── sales_processor.py           ← Broken CSV function (S1/M1 chat demo)
│   └── eda.py                       ← EDA script (/eda command target)
│
├── tests/
│   ├── test_sales_processor.py      ← Multi-turn test generation demo
│   └── test_api.py                  ← /review command demo target
│
├── data/
│   └── sales_sample.csv             ← Messy CSV (intentional bad rows)
│
└── .claude/
    └── commands/
        ├── review.md                ← /review slash command
        └── eda.md                   ← /eda slash command
```

---

## Common Demo Issues & Fixes

| Issue | Fix |
|-------|-----|
| `claude` command not found | `npm install -g @anthropic-ai/claude-code` |
| SQLite DB errors | `rm data/demo.db` then restart the server |
| FastAPI import errors | Check `pip install -r requirements.txt` completed |
| Worktree already exists | `git worktree remove ../demo-feature-branch --force` |
| Tests fail | `pytest tests/ -v --tb=long` to see full trace |
| uvicorn port in use | `uvicorn app.main:app --reload --port 8001` |
