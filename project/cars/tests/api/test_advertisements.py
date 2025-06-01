import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser
from cars.models import Advertisement

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return CustomUser.objects.create_user(
        email="test@user.com",
        username="testuser",  
        phone="+380991112233",
        password="testpass123"
    )

@pytest.fixture
def test_advertisement(test_user):
    return Advertisement.objects.create(
        user=test_user,
        title="Test Car",
        description="Test Description",
        price=15000.00,
        city="Kyiv",
        brand="Toyota",
        model_name="Camry",
        year=2020,
        body_type="sedan",
        drive_type="fwd",
        power=150,
        transmission="automatic",
        color="black",
        mileage=50000,
        door_count=4,
        fuel_type="petrol",
        engine_capacity=2.5,
        main_photo=None
    )

@pytest.mark.django_db
def test_create_advertisement(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    
    payload = {
        "title": "New Car 2023",
        "description": "Brand new car",
        "price": 30000,
        "city": "Lviv",
        "brand": "BMW",
        "model_name": "X5",
        "year": 2023,
        "body_type": "suv",
        "drive_type": "awd",
        "power": 300,
        "transmission": "automatic",
        "color": "white",
        "mileage": 0,
        "door_count": 5,
        "had_accidents": False,  
        "vin_code": "ABC123",
        "fuel_type": "petrol",
        "engine_capacity": 3.0
    }
    
    response = api_client.post(
        reverse("advertisements-list"),
        data=payload,
        format="json"
    )
    
    print(response.data)
    assert response.status_code == 415

@pytest.mark.django_db
def test_deactivate_advertisement(api_client, test_user, test_advertisement):
    api_client.force_authenticate(user=test_user)
    
    url = reverse("advertisements-deactivate", kwargs={"pk": test_advertisement.id})
    
    response = api_client.post(url)
    assert response.status_code == 200