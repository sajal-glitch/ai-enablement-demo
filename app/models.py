"""
Pydantic models for the Sales Analytics API.

These are the data shapes Claude needs to understand — used in:
  - CLAUDE.md exercise (Session 2 / Module 2): participants document these models
  - /review slash command demo (Session 2 / Module 3): Claude reviews this file
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    region: str
    created_at: Optional[str] = None

    # Intentionally missing validation — used in Session 2 / Module 1
    # Guided Practice: "Plan the addition of input validation to /users"


class Order(BaseModel):
    id: Optional[int] = None
    user_id: int
    product: str
    amount: float
    created_at: Optional[str] = None


class SalesRecord(BaseModel):
    id: Optional[int] = None
    date: str
    region: str
    revenue: float
    units: int
