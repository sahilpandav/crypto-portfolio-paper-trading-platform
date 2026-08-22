def _register_and_login(client, username="wallettester"):
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


def test_wallet_created_on_registration(client):
    token = _register_and_login(client)

    response = client.get(
        "/api/v1/wallet/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == "100000.00"


def test_wallet_requires_auth(client):
    response = client.get("/api/v1/wallet/me")
    assert response.status_code == 401