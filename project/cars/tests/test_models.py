from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import CustomUser
from cars.models import Advertisement, AdvertisementPhoto

class AdvertisementModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email='test@example.com', 
            password='password123'
        )
        
    def test_create_advertisement_valid(self):
        ad = Advertisement.objects.create(
            user=self.user,
            title="Test Car",
            description="Good condition",
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
            engine_capacity=2.5
        )
        self.assertEqual(ad.__str__(), "Toyota Camry (2020) - petrol 2.5л - 15000.00₴")

    def test_year_validator(self):
        with self.assertRaises(ValidationError):
            ad = Advertisement(
                user=self.user,
                year=1899,
                # інші обов'язкові поля...
            )
            ad.full_clean()
