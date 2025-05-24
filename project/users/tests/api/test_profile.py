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


# def test_update_user_profile(api_client, test_user):
#     api_client.force_authenticate(user=test_user)
    
#     # Update profile data
#     profile_data = {
#         'first_name': 'New',
#         'last_name': 'Name',
#         'profile': {
#             'phone': '+380991234567'
#         }
#     }
    
#     # Use PUT instead of PATCH since the endpoint doesn't accept PATCH
#     response = api_client.put(reverse('profile-me'), profile_data, format='json')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['first_name'] == 'New'
#     assert response.data['last_name'] == 'Name'
#     assert response.data['profile']['phone'] == '+380991234567'
    
#     # Verify the changes persisted
#     response = api_client.get(reverse('profile-me'))
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['first_name'] == 'New'
#     assert response.data['last_name'] == 'Name'


# def test_invalid_profile_data(api_client, test_user):
#     api_client.force_authenticate(user=test_user)
    
#     invalid_data = {
#         'profile': {
#             'phone': 'not-a-phone-number'
#         }
#     }
#     response = api_client.put(reverse('profile-me'), invalid_data, format='json')
#     assert response.status_code == status.HTTP_400_BAD_REQUEST