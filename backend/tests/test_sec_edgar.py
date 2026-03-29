from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.services.sec_edgar import (
    EdgarUnavailableError,
    TickerNotFoundError,
    facts_to_financial_years,
)

client = TestClient(app)


@pytest.fixture
def sec_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTO_RESEARCH_DATA_SOURCE", "sec")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_facts_to_financial_years_picks_latest_fy_per_year() -> None:
    facts = {
        "entityName": "Test Corp",
        "facts": {
            "us-gaap": {
                "RevenueFromContractWithCustomerExcludingAssessedTax": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-10-01",
                                "val": 1.0,
                            },
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 2.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 10.0,
                            },
                        ]
                    }
                },
                "GrossProfit": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 3.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 4.0,
                            },
                        ]
                    }
                },
                "OperatingIncomeLoss": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 1.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 1.0,
                            },
                        ]
                    }
                },
                "NetIncomeLoss": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 1.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 1.0,
                            },
                        ]
                    }
                },
                "Assets": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 100.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 90.0,
                            },
                        ]
                    }
                },
                "Liabilities": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 40.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 40.0,
                            },
                        ]
                    }
                },
                "StockholdersEquity": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 60.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 50.0,
                            },
                        ]
                    }
                },
                "CashAndCashEquivalentsAtCarryingValue": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 5.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 5.0,
                            },
                        ]
                    }
                },
                "LongTermDebt": {
                    "units": {
                        "USD": [
                            {
                                "fy": 2024,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2024-11-15",
                                "val": 20.0,
                            },
                            {
                                "fy": 2023,
                                "fp": "FY",
                                "form": "10-K",
                                "filed": "2023-11-01",
                                "val": 20.0,
                            },
                        ]
                    }
                },
            }
        },
    }
    name, rows = facts_to_financial_years(facts, anchor_year=2024, max_years=5)
    assert name == "Test Corp"
    assert [r["fiscal_year"] for r in rows] == [2023, 2024]
    assert rows[-1]["revenue"] == 2.0


def test_research_unknown_ticker_404(sec_mode: None) -> None:
    with patch(
        "app.services.sec_edgar.resolve_cik",
        side_effect=TickerNotFoundError("ZZZNOPE"),
    ):
        response = client.get("/api/v1/research/ZZZNOPE")
    assert response.status_code == 404


def test_research_sec_upstream_502(sec_mode: None) -> None:
    with patch(
        "app.services.sec_edgar.load_financial_history",
        side_effect=EdgarUnavailableError("SEC unreachable"),
    ):
        response = client.get("/api/v1/research/AAPL")
    assert response.status_code == 502
    assert "SEC" in response.json()["detail"]
