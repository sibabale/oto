from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_place_trade_accepts_order() -> None:
    response = client.post(
        "/api/v1/trades",
        json={"ticker": "AAPL", "side": "buy", "order_type": "market", "quantity": 10},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "accepted"
    assert body["broker"] == "paper"
    assert body["ticker"] == "AAPL"
    assert body["side"] == "buy"
    assert body["order_type"] == "market"
    assert body["quantity"] == 10


def test_limit_order_requires_limit_price() -> None:
    response = client.post(
        "/api/v1/trades",
        json={"ticker": "AAPL", "side": "buy", "order_type": "limit", "quantity": 1},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "TRADE_VALIDATION_ERROR"
