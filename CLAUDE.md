# CLAUDE.md — AI Enablement Demo Project

> This file is read automatically by Claude Code at the start of every session.
> Participants complete the [FILL IN] sections during the Session 2 / Module 2 exercise.

---

## Project Overview

This is a sample **Sales Analytics API** used for the AI Enablement Program Phase 1 demos.
It is a FastAPI service that exposes sales, user, and order data for internal analytics teams.
It is at the **prototype stage** — not yet in production.

---

## Tech Stack & Architecture

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** SQLite (demo) → PostgreSQL 15 (production)
- **Cache:** Redis (planned — see `app/cache.py`)
- **Testing:** pytest
- **Linting:** ruff
- **Deployment:** AWS ECS with Terraform (planned)

---

## Project Structure

```
ai-enablement-demo/
├── app/
│   ├── main.py           # FastAPI app, all route definitions
│   ├── models.py         # Pydantic request/response models
│   ├── database.py       # SQLite connection + seed data
│   ├── cache.py          # Redis cache layer (stub — implement in demo)
│   ├── sales_processor.py # CSV processing functions
│   └── eda.py            # EDA script (target for /eda slash command)
├── tests/
│   ├── test_sales_processor.py
│   └── test_api.py
├── data/
│   └── sales_sample.csv  # Sample data for demos
├── .claude/
│   └── commands/         # Custom slash command definitions
├── CLAUDE.md             # This file
├── README.md
└── requirements.txt
```

---

## Code Conventions

<!-- EXERCISE: fill in at least 3 conventions by reading the source files -->

- [FILL IN — e.g. "Use Google-style docstrings for all public functions"]
- [FILL IN — e.g. "All functions must have type hints"]
- [FILL IN — e.g. "Errors raised as HTTPException, not logged and swallowed"]

**Already defined:**
- Use `ruff` for linting. Run: `ruff check . --fix`
- Use `pytest` for tests. All test files in `/tests/`, mirroring `/app/` structure.
- Naming: `snake_case` for functions and variables, `PascalCase` for Pydantic models.
- Imports: stdlib → third-party → local (one blank line between groups).

---

## Testing Standards

- Framework: **pytest**
- Location: `/tests/` mirroring `/app/` structure
- Every public function needs: 1 happy path + 1 invalid input + 1 edge case
- No `mock.patch` — use dependency injection or `tmp_path` fixtures instead
- Run: `pytest tests/ -v`

---

## Guardrails & Constraints

<!-- EXERCISE: fill in at least 2 guardrails by reading the codebase -->

- [FILL IN — e.g. "Never commit directly to main"]
- [FILL IN — e.g. "Do not modify database.py seed data without approval"]

**Already defined:**
- **Never paste real customer data into any AI prompt.** Use synthetic data only.
- **Never commit secrets, tokens, or credentials.** Use `.env` files and `.gitignore`.
- Do not modify `data/sales_sample.csv` — it is the shared demo fixture.
- Do not implement the Redis cache layer without running plan mode first (see `app/cache.py`).

---

## Common Commands

<!-- EXERCISE: fill in at least 3 commands by reading this project -->

- [FILL IN — e.g. "Run tests: pytest tests/ -v"]
- [FILL IN — e.g. "Start dev server: uvicorn app.main:app --reload"]
- [FILL IN — e.g. "Lint: ruff check . --fix"]

**Already defined:**
```bash
# Start dev server
uvicorn app.main:app --reload

# Run all tests
pytest tests/ -v

# Run tests with short output (good for demo)
pytest tests/ -v --tb=short

# Lint
ruff check . --fix

# Run EDA on sample data
python app/eda.py data/sales_sample.csv

# Seed the database
python -c "from app.database import get_db_connection; get_db_connection()"
```

---

## Demo Map

| Session | Module | File(s) to open | What Claude does |
|---------|--------|-----------------|-----------------|
| S1 / M1 | Claude Chat demo | `app/sales_processor.py` | Refactors broken function, adds tests |
| S1 / M1 | Claude Code terminal | `app/main.py` | Adds `/health` endpoint |
| S2 / M1 | Plan Mode | `app/cache.py` | Plans Redis caching layer |
| S2 / M1 | Guided Practice | `app/main.py` → `/users` | Plans input validation |
| S2 / M2 | CLAUDE.md exercise | This file | Participants fill [FILL IN] sections |
| S2 / M3 | `/review` command | `tests/test_api.py` | Reviews for coverage gaps |
| S2 / M3 | `/eda` command | `data/sales_sample.csv` | Runs standardised EDA |
| S2 / M4 | Worktrees | Whole repo | Two terminals, two branches |
