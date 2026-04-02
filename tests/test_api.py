"""
API endpoint tests.

DEMO USAGE:
  Session 2 / Module 3 — /review slash command demo:
    Highlight this file in VS Code and run /review.
    Claude will flag: missing auth tests, no rate-limit tests, etc.

  Run:
    pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUsersEndpoint:

    def test_list_users_returns_200(self):
        response = client.get("/users")
        assert response.status_code == 200

    def test_list_users_returns_list(self):
        response = client.get("/users")
        assert isinstance(response.json(), list)

    def test_list_users_filter_by_region(self):
        response = client.get("/users?region=APAC")
        data = response.json()
        assert all(u["region"] == "APAC" for u in data)

    def test_get_user_returns_404_for_missing_id(self):
        response = client.get("/users/99999")
        assert response.status_code == 404

    def test_get_user_returns_correct_user(self):
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1


class TestOrdersEndpoint:

    def test_list_orders_returns_200(self):
        response = client.get("/orders")
        assert response.status_code == 200

    def test_create_order_returns_201(self):
        payload = {"user_id": 1, "product": "Test Product", "amount": 99.99}
        response = client.post("/orders", json=payload)
        assert response.status_code == 201


class TestSalesSummary:

    def test_sales_summary_returns_200(self):
        response = client.get("/sales/summary")
        assert response.status_code == 200

    def test_sales_summary_filter_by_region(self):
        response = client.get("/sales/summary?region=APAC")
        data = response.json()
        assert all(r["region"] == "APAC" for r in data)
