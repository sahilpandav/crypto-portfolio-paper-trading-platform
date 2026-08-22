from unittest.mock import patch
from decimal import Decimal


def _register_and_login(client, username="trader"):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpassword123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "testpassword123"},
    )
    return login_response.json()["access_token"]


@patch("app.services.trade_service.get_current_price")
def test_buy_success(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    response = client.post(
        "/api/v1/trade/buy",
        json={"coin_symbol": "BTC", "quantity": "0.1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["coin_symbol"] == "BTC"
    assert data["trade_type"] == "BUY"
    assert data["price_at_trade"] == "60000.00"
    assert data["total_value"] == "6000.00"


@patch("app.services.trade_service.get_current_price")
def test_buy_reduces_wallet_balance(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    client.post(
        "/api/v1/trade/buy",
        json={"coin_symbol": "BTC", "quantity": "0.1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/v1/wallet/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json()["balance"] == "94000.00"


@patch("app.services.trade_service.get_current_price")
def test_buy_insufficient_balance(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    response = client.post(
        "/api/v1/trade/buy",
        json={"coin_symbol": "BTC", "quantity": "1000"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient wallet balance for this trade."


@patch("app.services.trade_service.get_current_price")
def test_sell_success(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    client.post(
        "/api/v1/trade/buy",
        json={"coin_symbol": "BTC", "quantity": "0.1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.post(
        "/api/v1/trade/sell",
        json={"coin_symbol": "BTC", "quantity": "0.05"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["trade_type"] == "SELL"


@patch("app.services.trade_service.get_current_price")
def test_sell_insufficient_holdings(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    response = client.post(
        "/api/v1/trade/sell",
        json={"coin_symbol": "BTC", "quantity": "1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient holdings for this trade."


@patch("app.services.trade_service.get_current_price")
def test_full_sell_removes_holding(mock_price, client):
    mock_price.return_value = Decimal("60000.00")
    token = _register_and_login(client)

    client.post(
        "/api/v1/trade/buy",
        json={"coin_symbol": "BTC", "quantity": "0.1"},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/v1/trade/sell",
        json={"coin_symbol": "BTC", "quantity": "0.1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/v1/portfolio/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json() == []