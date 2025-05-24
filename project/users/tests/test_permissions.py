from django.test import TestCase, RequestFactory
from users.models import CustomUser, Favorites
from users.api.permissions import IsOwnerOrReadOnly, IsOwner

class PermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            email='user@example.com', 
            username='testuser',  
            password='testpass',
            phone='+1234567890'
        )

    def test_is_owner_permission(self):
        permission = IsOwner()
        request = self.factory.get('/')
        request.user = self.user
        

    def test_is_owner_or_read_only(self):
        permission = IsOwnerOrReadOnly()
        request = self.factory.delete('/')
        request.user = CustomUser.objects.create_user(
            email='other@example.com', 
            username='otheruser',
            password='testpass'
        )
