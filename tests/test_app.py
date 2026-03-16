import json
import pytest
from quote_service.app import create_app


@pytest.fixture
def client():
    app = create_app(instance_name="test-instance")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["status"] == "healthy"


def test_quote_returns_valid_json(client):
    resp = client.get("/quote")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert "quote" in data
    assert "book" in data
    assert "instance" in data
    assert data["instance"] == "test-instance"


def test_quote_returns_different_quotes(client):
    quotes = set()
    for _ in range(50):
        resp = client.get("/quote")
        data = json.loads(resp.data)
        quotes.add(data["quote"])
    assert len(quotes) > 1
