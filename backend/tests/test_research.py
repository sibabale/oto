from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.services.research_service import get_company_research

client = TestClient(app)


def test_research_returns_last_five_fiscal_years() -> None:
    response = client.get("/api/v1/research/AAPL")
    assert response.status_code == 200

    payload = response.json()
    assert payload["ticker"] == "AAPL"
    assert len(payload["years"]) == 5
    assert "score" in payload

    anchor = date.today().year
    expected_years = [anchor - i for i in range(5)]
    assert [y["fiscal_year"] for y in payload["years"]] == expected_years


def test_research_window_anchored_to_year() -> None:
    result = get_company_research("MSFT", anchor_year=2026)
    assert [y.fiscal_year for y in result.years] == [2026, 2025, 2024, 2023, 2022]
