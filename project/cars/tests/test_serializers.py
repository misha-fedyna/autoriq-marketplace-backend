from django.test import TestCase
from rest_framework.exceptions import ValidationError
from cars.api.serializers import AdvertisementCreateUpdateSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
import os

class AdvertisementSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="serializer@test.com",
            username="serializeruser",
            phone="+380992223344",
            password="testpass"
        )

    def test_valid_data(self):
        payload = {
            "title": "Valid Car",
            "description": "Valid description",
            "price": 20000,
            "city": "Kharkiv",
            "brand": "Audi",
            "model_name": "A6",
            "year": 2019,
            "body_type": "sedan",
            "drive_type": "awd",
            "power": 249,
            "transmission": "automatic",
            "color": "silver",
            "mileage": 60000,
            "door_count": 4,
            "had_accidents": False,
            "vin_code": "VINCODE1234567890",
            "fuel_type": "diesel",
            "engine_capacity": 3.0,
        }
        serializer = AdvertisementCreateUpdateSerializer(data=payload)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_field(self):
        payload = {
            "title": "Missing Fields Car",
            "price": 10000,
        }
        serializer = AdvertisementCreateUpdateSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("brand", serializer.errors)
        self.assertIn("model_name", serializer.errors)
        self.assertIn("year", serializer.errors)

    def test_invalid_engine_capacity(self):
        payload = {
            "title": "Invalid Engine Car",
            "description": "Test",
            "price": 30000,
            "city": "Dnipro",
            "brand": "Mercedes",
            "model_name": "E-Class",
            "year": 2020,
            "body_type": "sedan",
            "drive_type": "rwd",
            "power": 220,
            "transmission": "automatic",
            "color": "black",
            "mileage": 40000,
            "door_count": 4,
            "fuel_type": "petrol",
            "engine_capacity": 10.5,  # Занадто велике значення
        }
        serializer = AdvertisementCreateUpdateSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("engine_capacity", serializer.errors)