from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/users/', include('users.api.urls')),
    path('api/cars/', include('cars.api.urls')),
    path('api/reviews/', include('reviews.api.urls')),
]