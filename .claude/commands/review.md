# /review — Code Review Command

Perform a thorough code review of the current file or the file I specify.

## Instructions

Review the target file for the following categories. For each issue found,
state the category, the line number(s), what the problem is, and what to do
instead. If no issues are found in a category, write "None found."

### Categories to check

1. **Correctness** — Logic errors, off-by-one errors, wrong assumptions
2. **Security** — Any hardcoded secrets, SQL injection risk, unvalidated input
3. **Error handling** — Unhandled exceptions, missing status codes, swallowed errors
4. **Test coverage gaps** — What is NOT tested that should be
5. **Type safety** — Missing type hints, incorrect types, Any overuse
6. **Performance** — N+1 queries, missing indexes, unnecessary loops
7. **Code conventions** — PEP 8, naming, docstrings (per CLAUDE.md standards)

## Output format

```
## Review: {filename}

### Correctness
- Line X: [issue] → [recommendation]

### Security
- Line X: [issue] → [recommendation]

... (all 7 categories)

### Summary
X issues found. Priority fixes: [list top 3]
```

## Usage examples

```
/review                          # Reviews the current open file
/review tests/test_api.py        # Reviews a specific file
/review app/main.py              # Reviews the main API routes
```
