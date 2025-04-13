from django.contrib import admin
from .models import Brand, CarModel, BodyType, Color, CarProduct, Advertisement

admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(BodyType)
admin.site.register(Color)
admin.site.register(CarProduct)
admin.site.register(Advertisement)