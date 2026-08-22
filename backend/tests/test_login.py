def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "testpassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "loginuser", "password": "testpassword123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "testpassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "loginuser", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password."


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "ghost", "password": "whatever123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password."


def test_protected_route_requires_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_protected_route_with_valid_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "meuser@example.com",
            "password": "testpassword123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "meuser", "password": "testpassword123"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "meuser"