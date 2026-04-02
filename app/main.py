"""
AI Enablement Demo — FastAPI Application
=========================================
This is the sample project used across both Phase 1 sessions.

Demo points this file enables:
  Session 1 / Module 1  — Claude Code terminal demo: add a /health endpoint
  Session 2 / Module 1  — Plan Mode demo: add Redis caching to read endpoints
  Session 2 / Module 1  — Guided practice: add input validation to /users
  Session 2 / Module 2  — CLAUDE.md exercise: participants read this file to understand the project
  Session 2 / Module 3  — /review slash command demo target
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from app.models import User, Order, SalesRecord
from app.database import get_db_connection
from app import __version__

app = FastAPI(
    title="Sales Analytics API",
    description="Internal API for querying sales and user data.",
    version=__version__,
)


# ─────────────────────────────────────────────────────────────────────────────
# DEMO TARGET 1 (Session 1 / Module 1 — Claude Code Terminal Demo)
# Ask Claude Code: "Add a GET /health endpoint that returns the application
# version and current timestamp."
# Expected output: Claude proposes a diff adding the /health route below.
# ─────────────────────────────────────────────────────────────────────────────

# ── Intentionally left blank so Claude Code can add it live ──
# Facilitator: leave this comment visible on screen before running Claude Code.


# ─────────────────────────────────────────────────────────────────────────────
# EXISTING ENDPOINTS — read-heavy (targets for Redis caching in Session 2)
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/users", response_model=list[User], tags=["Users"])
async def list_users(
    region: Optional[str] = Query(None, description="Filter by region"),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Return a paginated list of users, optionally filtered by region.

    This is one of the three read-heavy endpoints targeted for Redis caching
    in the Session 2 / Module 1 Plan Mode demo.
    """
    conn = get_db_connection()
    query = "SELECT * FROM users"
    params = []
    if region:
        query += " WHERE region = ?"
        params.append(region)
    query += f" LIMIT {limit}"
    rows = conn.execute(query, params).fetchall()
    return [User(**dict(r)) for r in rows]


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """
    Return a single user by ID.

    Guided Practice target (Session 2 / Module 1):
    'Plan the addition of input validation to the /users endpoint.
    The endpoint currently accepts any JSON body without validation.'
    """
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", [user_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return User(**dict(row))


@app.get("/orders", response_model=list[Order], tags=["Orders"])
async def list_orders(
    user_id: Optional[int] = Query(None),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Return orders, optionally filtered by user_id.

    Read-heavy endpoint — targeted for Redis caching in Session 2 / Module 1.
    """
    conn = get_db_connection()
    query = "SELECT * FROM orders"
    params = []
    if user_id:
        query += " WHERE user_id = ?"
        params.append(user_id)
    query += f" LIMIT {limit}"
    rows = conn.execute(query, params).fetchall()
    return [Order(**dict(r)) for r in rows]


@app.get("/sales/summary", tags=["Sales"])
async def sales_summary(
    region: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
):
    """
    Return aggregate sales summary grouped by region and quarter.

    Read-heavy endpoint — targeted for Redis caching in Session 2 / Module 1.
    This endpoint is intentionally slow (no index on region + year) to make
    the caching benefit obvious during the demo.
    """
    conn = get_db_connection()
    query = """
        SELECT
            region,
            strftime('%Y', date) AS year,
            strftime('%m', date) AS month,
            SUM(revenue)         AS total_revenue,
            SUM(units)           AS total_units
        FROM sales_records
    """
    conditions, params = [], []
    if region:
        conditions.append("region = ?")
        params.append(region)
    if year:
        conditions.append("strftime('%Y', date) = ?")
        params.append(str(year))
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY region, year, month ORDER BY year, month"
    rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


@app.post("/orders", tags=["Orders"])
async def create_order(order: Order):
    """Write endpoint — NOT a candidate for read-through caching."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO orders (user_id, product, amount, created_at) VALUES (?, ?, ?, ?)",
        [order.user_id, order.product, order.amount, datetime.utcnow().isoformat()],
    )
    conn.commit()
    return JSONResponse(status_code=201, content={"message": "Order created"})
