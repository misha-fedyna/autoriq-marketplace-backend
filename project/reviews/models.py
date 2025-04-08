# reviews/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import CustomUser
from cars.models import CarProduct

class Review(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews"  # user.reviews.all()
    )
    car_product = models.ForeignKey(
        CarProduct,
        on_delete=models.CASCADE,
        related_name="reviews"  # car_product.reviews.all()
    )
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'car_product')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"Review {self.id} by {self.user.email}"