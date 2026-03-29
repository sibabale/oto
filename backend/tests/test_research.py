from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_research_returns_five_years() -> None:
    response = client.get("/api/v1/research/AAPL")
    assert response.status_code == 200

    payload = response.json()
    assert payload["ticker"] == "AAPL"
    assert len(payload["years"]) == 5
    assert "score" in payload
