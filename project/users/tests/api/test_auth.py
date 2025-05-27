import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_jwt_login(api_client, test_user):
    response = api_client.post(reverse('jwt-create'), {
        "email": test_user.email,
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert 'access' in response.data


def test_jwt_login_invalid_credentials(api_client, test_user):
    response = api_client.post(reverse('jwt-create'), {
        "email": test_user.email,
        "password": "wrong_password"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_jwt_refresh(api_client, test_user):
    # First login to get the refresh token
    login_response = api_client.post(reverse('jwt-create'), {
        "email": test_user.email,
        "password": "testpass123"
    })
    refresh_token = login_response.data['refresh']
    
    # Use the refresh token to get a new access token
    response = api_client.post(reverse('jwt-refresh'), {
        "refresh": refresh_token
    })
    assert response.status_code == 200
    assert 'access' in response.data


def test_jwt_verify(api_client, test_user):
    # First login to get the token
    login_response = api_client.post(reverse('jwt-create'), {
        "email": test_user.email,
        "password": "testpass123"
    })
    token = login_response.data['access']
    
    # Verify the token
    response = api_client.post(reverse('jwt-verify'), {
        "token": token
    })
    assert response.status_code == 200