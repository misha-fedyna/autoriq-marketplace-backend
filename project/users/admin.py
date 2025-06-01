from django.contrib import admin
from .models import CustomUser, UserProfile, Favorites

"""
This module registers the CustomUser, UserProfile, and Favorites models with the Django admin site,
enabling their management through the Django admin interface.
Usage:
    The registered models will be accessible and manageable via the Django admin dashboard.
"""

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Favorites)