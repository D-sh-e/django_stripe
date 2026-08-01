from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name = 'Название')
    description = models.TextField(blank=True, verbose_name = 'Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена (USD)')
  