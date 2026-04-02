"""
Cache Layer — Redis Integration
=================================
STATUS: NOT YET IMPLEMENTED — this is the DEMO TARGET for Session 2 / Module 1.

PLAN MODE DEMO (Session 2 / Module 1):
  Use this prompt in Claude Code with plan mode:

  "I need to add a caching layer to our API. We have a FastAPI service with
  5 endpoints that query a SQLite/PostgreSQL database. I want to add Redis
  caching for the 3 read-heavy endpoints (/users, /orders, /sales/summary),
  with configurable TTL per endpoint and cache invalidation when the underlying
  data changes. Use plan mode to plan this before implementing."

  After Claude generates the plan, CHALLENGE ASSUMPTIONS:
    → "Why Redis over in-memory caching?"
    → "What happens during a Redis outage — does the API go down?"
    → "How do we invalidate the cache when an order is created?"

  Refine the plan by asking:
    "Add a fallback strategy for Redis failures before implementing."

  Only AFTER the plan is approved, switch to implementation.
  Expected: Claude will fill in this file with a working Redis cache layer.

WHAT A GOOD PLAN LOOKS LIKE:
  Files to modify: app/main.py (add cache.get/set calls around DB queries)
  Files to create:  app/cache.py (this file — TTL config, get/set/invalidate)
  Dependencies:     redis-py, add to requirements.txt
  Order:            1. cache.py → 2. integrate into /users → 3. /orders →
                    4. /sales/summary → 5. add invalidation to POST /orders
  Fallback:         if Redis unreachable, log warning and query DB directly
"""

import os
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Per-endpoint TTL configuration (seconds)
# Facilitator: show this as the "configurable TTL" requirement in the plan
CACHE_TTL = {
    "users":         60,    # 1 minute — user data changes infrequently
    "orders":        30,    # 30 seconds — orders change more often
    "sales_summary": 300,   # 5 minutes — aggregates are expensive, change rarely
}

# ── TODO: implement with Redis ──────────────────────────────────────────────
# The functions below are stubs. Claude Code will implement them during demo.

def get_cache_client():
    """
    Return a Redis client, or None if Redis is unavailable.

    Fallback strategy: if Redis is not reachable, return None and let callers
    fall through to the database. The API never goes down due to Redis.
    """
    # TODO: implement
    raise NotImplementedError("Implement during Plan Mode demo")


def cache_get(key: str) -> Optional[Any]:
    """Retrieve a value from cache. Returns None on miss or Redis unavailability."""
    # TODO: implement
    raise NotImplementedError("Implement during Plan Mode demo")


def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    """Store a value in cache with a TTL. Silently skips if Redis unavailable."""
    # TODO: implement
    raise NotImplementedError("Implement during Plan Mode demo")


def cache_invalidate(pattern: str) -> None:
    """
    Delete all cache keys matching a pattern.

    Called from POST /orders to invalidate /orders and /sales/summary caches.
    """
    # TODO: implement
    raise NotImplementedError("Implement during Plan Mode demo")


def make_cache_key(endpoint: str, **kwargs) -> str:
    """Build a deterministic cache key from endpoint name and query parameters."""
    params = "&".join(f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None)
    return f"demo:{endpoint}:{params}" if params else f"demo:{endpoint}"
