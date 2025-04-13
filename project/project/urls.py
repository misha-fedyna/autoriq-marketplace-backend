from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/', include('users.api.urls')),
    path('api/cars/', include('cars.api.urls')),
    path('api/reviews/', include('reviews.api.urls')),
]