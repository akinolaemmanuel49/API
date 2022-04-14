from tests.test_api import client, status


def test_create_user():
    response = client.post(
        "/users/", json={"username": "testuser0", "email": "testuser0@mail.com", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_duplicate_email():
    response = client.post(
        "/users/", json={"username": "testuser1", "email": "testuser0@mail.com", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_duplicate_username():
    response = client.post(
        "/users/", json={"username": "testuser0", "email": "testuser1@mail.com", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_missing_username_field():
    response = client.post(
        "/users/", json={"email": "testuser1mail.com", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_missing_email_field():
    response = client.post(
        "/users/", json={"username": "testuser1", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_missing_password_field():
    response = client.post(
        "/users/", json={"username": "testuser1", "email": "testuser1mail.com"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_validate_email():
    response = client.post(
        "/users/", json={"username": "testuser1", "email": "testuser1mail.com", "password": "password", "confirm_password": "password"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK


def test_login():
    response = client.post(
        "/users/login", json={"username": "testuser0", "password": "password"})
    assert response.status_code == status.HTTP_200_OK


def test_login_missing_username():
    response = client.post(
        "/users/login", json={"password": "password"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_missing_password():
    response = client.post(
        "/users/login", json={"username": "testuser0"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_user():
    auth_token = client.post(
        "/users/login", json={"username": "testuser0", "password": "password"}
    ).json()
    response = client.delete(
        "/users/?username=testuser0", headers={"Authorization": f"Bearer {auth_token['access_token']}"})
    assert response.status_code == status.HTTP_200_OK
