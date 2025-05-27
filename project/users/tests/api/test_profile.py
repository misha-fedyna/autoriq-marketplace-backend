import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_get_user_profile(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get(reverse('profile-me'))
    assert response.status_code == 200
    assert response.data['email'] == test_user.email
    assert 'profile' in response.data


def test_unauthorized_profile_access(api_client):
    # Test accessing profile without authentication
    response = api_client.get(reverse('profile-me'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
