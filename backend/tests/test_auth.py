def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "first@example.com",
            "password": "testpassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "second@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username is already taken."


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "userone",
            "email": "same@example.com",
            "password": "testpassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "usertwo",
            "email": "same@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email is already registered."


def test_register_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "not-an-email",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 422


def test_register_password_too_short(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422