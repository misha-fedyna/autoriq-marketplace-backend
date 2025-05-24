from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserProfile, Favorites

CustomUser = get_user_model()

class UserModelsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            phone='+1234567890',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.phone, '+1234567890')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_profile_relationship(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile.first_name, 'John')

