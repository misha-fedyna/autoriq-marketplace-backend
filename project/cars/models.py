from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datatime
from users.models import CustomUser

class Brand(models.Model):
    brancd_name = models.CharField("Brand", max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    founded_year = models.models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1886),
            MaxValueValidator(datetime.now().year)
        ]
    )
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["brand_name"]

    def __str__(self):
        return self.brand_name

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, ralated_name="models")
    model_name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.brand.brand_name} {self.model_name}"


class BodyType(models.Model):
    body_type_name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.body_type_name


class CarProduct(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=60)
    mileage = models.IntegerField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Advertisement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car_product = models.ForeignKey(CarProduct, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Advertisement for {self.car_product} by {self.user.email}"
