from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser
from cars.models import Advertisement, AdvertisementPhoto
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class AdvertisementModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone="+1234567890",
            password="testpass123"
        )
        
        self.ad = Advertisement.objects.create(
            user=self.user,
            title="Test Car",
            description="Test Description",
            price=10000.00,
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
            had_accidents=False,
            vin_code="ABCDEFGHJKLMNOPQR",
            fuel_type="petrol",
            engine_capacity=2.5,
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.brand, "Toyota")
        self.assertEqual(self.ad.get_fuel_type_display(), "Бензин")
        self.assertTrue(self.ad.is_active)
        self.assertEqual(self.ad.user.email, "test@example.com")

    def test_price_validation(self):
        with self.assertRaises(ValidationError):
            invalid_ad = Advertisement(
                user=self.user,
                title="Invalid Car",
                description="Invalid",
                price=-100,
                city="Kyiv",
                brand="Toyota",
                model_name="Corolla",
                year=2020,
                body_type="sedan",
                drive_type="fwd",
                power=120,
                transmission="automatic",
                color="white",
                mileage=30000,
                door_count=4,
                fuel_type="petrol",
                engine_capacity=1.8
            )
            invalid_ad.full_clean()

    def test_year_validation(self):
        with self.assertRaises(ValidationError):
            invalid_ad = Advertisement(
                user=self.user,
                title="Old Car",
                description="Too old",
                price=5000,
                city="Lviv",
                brand="Ford",
                model_name="Model T",
                year=1899,
                body_type="sedan",
                drive_type="rwd",
                power=20,
                transmission="manual",
                color="black",
                mileage=999999,
                door_count=2,
                fuel_type="petrol",
                engine_capacity=2.9
            )
            invalid_ad.full_clean()