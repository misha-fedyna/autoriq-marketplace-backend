from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser, UserProfile
from .serializers import UserSerializer, RegistrationSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "message": "User registered successfully",
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Regular users can only see themselves
        if not self.request.user.is_staff:
            return CustomUser.objects.filter(id=self.request.user.id)
        return super().get_queryset()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        if not user.check_password(request.data.get('old_password')):
            return Response({"old_password": ["Wrong password."]}, 
                            status=status.HTTP_400_BAD_REQUEST)
                            
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({"status": "password set"}, status=status.HTTP_200_OK)
