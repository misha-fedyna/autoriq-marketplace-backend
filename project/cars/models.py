from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from users.models import CustomUser

class Brand(models.Model):
    brand_name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True, null=True)
    founded_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1886),
            MaxValueValidator(timezone.now().year) 
        ]
    )
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["brand_name"]

    def __str__(self):
        return self.brand_name

class CarModel(models.Model):
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE, 
        related_name="car_models"
    )
    model_name = models.CharField(max_length=60)

    class Meta:
        unique_together = ('brand', 'model_name')
        ordering = ['model_name']
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"

    def __str__(self):
        return f"{self.brand.brand_name} {self.model_name}"


class BodyType(models.Model):
    body_type_name = models.CharField("Body Type", max_length=60, unique=True)

    class Meta:
        verbose_name = "Body Type"
        verbose_name_plural = "Body Types"
    
    def __str__(self):
        return self.body_type_name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class CarProduct(models.Model):
    model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE, 
        related_name='car_products'
    )
    body_type = models.ForeignKey(
        BodyType, 
        on_delete=models.CASCADE, 
        related_name='cars'
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year)
        ],
        db_index=True
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        db_index=True
    )
    color = models.ForeignKey(
        Color, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    mileage = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['year', 'price']),
            models.Index(fields=['mileage']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.price}$"


class Advertisement(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, 
        related_name="adverstisements"
    )
    car_product = models.ForeignKey(
        CarProduct, 
        on_delete=models.CASCADE,
        related_name="advertisements"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, db_index=True)
    approved_by = models.ForeignKey(
        CustomUser, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name="approved_advertisements"
        )
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        status = "Active" if self.is_active else "Deleted"
        return f"{self.title} ({status})"
