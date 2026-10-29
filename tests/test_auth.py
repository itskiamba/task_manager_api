from tests.conftest import make_user


def test_register_and_login(client):
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "Bob@Example.com", "full_name": "Bob", "password": "supersecret1"},
    )
    assert r.status_code == 201
    assert r.json()["email"] == "bob@example.com"  # emails are lowercased
    assert "password" not in r.json()
    assert "hashed_password" not in r.json()


def test_duplicate_email_rejected(client):
    make_user(client)
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "full_name": "A", "password": "supersecret1"},
    )
    assert r.status_code == 409


def test_wrong_password(client):
    make_user(client)
    r = client.post(
        "/api/v1/auth/login", data={"username": "alice@example.com", "password": "nope"}
    )
    assert r.status_code == 401


def test_short_password_rejected(client):
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "x@example.com", "full_name": "X", "password": "short"},
    )
    assert r.status_code == 422


def test_me_requires_token(client, auth):
    assert client.get("/api/v1/users/me").status_code == 401  # no token

    r = client.get("/api/v1/users/me", headers=auth)  # with token
    assert r.status_code == 200
    assert r.json()["email"] == "alice@example.com"