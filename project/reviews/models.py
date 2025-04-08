from django.db import models
from users.models import CustomUser
from cars.models import CarProduct

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car_product = models.ForeignKey(CarProduct, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car_product')

    def __str__(self):
        return f"Review by {self.user.email} for {self.car_product}"
