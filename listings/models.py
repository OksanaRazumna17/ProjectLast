from django.db import models
from django.contrib.auth.models import User


# Создание модели объявления
class Listing(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('land', 'Земля'),
    ]

    title = models.CharField(max_length=200)  # Заголовок объявления
    description = models.TextField()  # Описание недвижимости
    location = models.CharField(max_length=200)  # Местоположение
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    rooms = models.PositiveIntegerField()  # Количество комнат
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)  # Тип жилья
    is_active = models.BooleanField(default=True)  # Статус объявления (активно/неактивно)
    owner = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)  # Владелец объявления

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
