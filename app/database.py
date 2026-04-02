"""
Database connection helper.

Uses SQLite so the demo works without any external database setup.
In production this would be PostgreSQL 15 (documented in CLAUDE.md).

SQLite DB is auto-created and seeded on first connection — see seed_db().
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "demo.db"


def get_db_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row_factory set to dict-like rows."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    if not _is_seeded(conn):
        seed_db(conn)
    return conn


def _is_seeded(conn: sqlite3.Connection) -> bool:
    try:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        return count > 0
    except sqlite3.OperationalError:
        return False


def seed_db(conn: sqlite3.Connection) -> None:
    """Create tables and insert sample data for demo purposes."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            email      TEXT    NOT NULL UNIQUE,
            region     TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS orders (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            product    TEXT    NOT NULL,
            amount     REAL    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS sales_records (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            date    TEXT    NOT NULL,
            region  TEXT    NOT NULL,
            revenue REAL    NOT NULL,
            units   INTEGER NOT NULL
        );
    """)

    users = [
        ("Priya Sharma",   "priya@example.com",   "APAC"),
        ("Rohan Mehta",    "rohan@example.com",   "APAC"),
        ("Aisha Patel",    "aisha@example.com",   "EMEA"),
        ("James Wilson",   "james@example.com",   "NA"),
        ("Sara Lin",       "sara@example.com",    "APAC"),
        ("Carlos Rivera",  "carlos@example.com",  "LATAM"),
        ("Nina Gupta",     "nina@example.com",    "EMEA"),
        ("Tom Baker",      "tom@example.com",     "NA"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO users (name, email, region) VALUES (?, ?, ?)", users
    )

    orders = [
        (1, "Analytics Pro",  1200.00),
        (1, "Data Starter",    299.00),
        (2, "Analytics Pro",  1200.00),
        (3, "Enterprise Suite",4500.00),
        (4, "Data Starter",    299.00),
        (5, "Analytics Pro",  1200.00),
        (6, "Enterprise Suite",4500.00),
        (7, "Analytics Pro",  1200.00),
        (8, "Data Starter",    299.00),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO orders (user_id, product, amount) VALUES (?, ?, ?)", orders
    )

    import random
    random.seed(42)
    regions = ["APAC", "EMEA", "NA", "LATAM"]
    records = []
    for year in [2023, 2024]:
        for month in range(1, 13):
            for region in regions:
                date = f"{year}-{month:02d}-01"
                revenue = round(random.uniform(20000, 120000), 2)
                units = random.randint(50, 400)
                records.append((date, region, revenue, units))
    conn.executemany(
        "INSERT INTO sales_records (date, region, revenue, units) VALUES (?, ?, ?, ?)",
        records,
    )
    conn.commit()
