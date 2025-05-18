from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from cloudinary.models import CloudinaryField
from users.models import CustomUser

class Advertisement(models.Model):
    # Вибір значень для певних полів
    BODY_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('hatchback', 'Хетчбек'),
        ('suv', 'Позашляховик'),
        ('wagon', 'Універсал'),
        ('coupe', 'Купе'),
        ('convertible', 'Кабріолет'),
        ('van', 'Мінівен'),
        ('pickup', 'Пікап'),
    ]
    
    DRIVE_TYPE_CHOICES = [
        ('fwd', 'Передній'),
        ('rwd', 'Задній'),
        ('awd', 'Повний'),
        ('4wd', '4WD'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Механічна'),
        ('automatic', 'Автоматична'),
        ('cvt', 'Варіатор'),
        ('semi-auto', 'Роботизована'),
    ]
    
    COLOR_CHOICES = [
        ('white', 'Білий'),
        ('black', 'Чорний'),
        ('silver', 'Срібний'),
        ('gray', 'Сірий'),
        ('red', 'Червоний'),
        ('blue', 'Синій'),
        ('green', 'Зелений'),
        ('yellow', 'Жовтий'),
        ('brown', 'Коричневий'),
        ('orange', 'Помаранчевий'),
        ('purple', 'Фіолетовий'),
        ('beige', 'Бежевий'),
    ]
    
    # Базова інформація про оголошення
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="advertisements")
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    city = models.CharField(max_length=100)
    
    # Інформація про автомобіль
    brand = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(validators=[
        MinValueValidator(1900), 
        MaxValueValidator(timezone.now().year)
    ])
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    drive_type = models.CharField(max_length=10, choices=DRIVE_TYPE_CHOICES)
    power = models.PositiveIntegerField(help_text="Потужність двигуна в к.с.")
    transmission = models.CharField(max_length=15, choices=TRANSMISSION_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    mileage = models.PositiveIntegerField()
    door_count = models.PositiveSmallIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    had_accidents = models.BooleanField(default=False, help_text="Чи була машина в ДТП")
    vin_code = models.CharField(max_length=17, blank=True, null=True)
    
    # Основна фотографія
    main_photo = CloudinaryField('main_photo', blank=True, null=True)
    
    # Службова інформація
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'is_active']),
            models.Index(fields=['brand', 'price']),
            models.Index(fields=['year', 'price']),
            models.Index(fields=['city', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year}) - {self.price}₴"

class AdvertisementPhoto(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="photos")
    photo = CloudinaryField('photo')
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Фото {self.order} для {self.advertisement}"