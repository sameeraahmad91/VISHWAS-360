from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient

pytest.importorskip("supabase")
from backend import main

class FakeResult:
    data = []
    count = 0

class FakeTable:
    def __init__(self, name): self.name = name
    def __getattr__(self, _): return lambda *a, **k: self
    def execute(self): return FakeResult()

class FakeDB:
    def table(self, name): return FakeTable(name)

@pytest.fixture(autouse=True)
def fake_db(monkeypatch):
    monkeypatch.setattr(main, "supabase", FakeDB())

def test_health_is_available():
    response = TestClient(main.app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"healthy", "degraded"}

def test_booking_rejects_past_date():
    response = TestClient(main.app).post("/bookings", json={"customer_id":"u", "service_id":1, "booking_date":str(date.today()-timedelta(days=1)), "booking_time":"10:00", "address":"Some address"})
    assert response.status_code == 422
