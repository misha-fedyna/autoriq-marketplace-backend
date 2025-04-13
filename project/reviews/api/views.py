from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Review
from .serializers import ReviewSerializer
from users.api.permissions import IsOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['car_product', 'rating']
    ordering_fields = ['created_at', 'rating']
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        reviews = Review.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_car(self, request):
        car_id = request.query_params.get('car_product', None)
        if car_id:
            reviews = Review.objects.filter(car_product_id=car_id)
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data)
        return Response({"error": "car_product parameter is required"}, status=400)