import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_user():
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        phone="+1234567890",
        username="testuser"
    )