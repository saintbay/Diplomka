from pydoc import describe
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings     

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    age = models.IntegerField(null=True, blank=True, verbose_name='Возраст')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')

    def __str__(self):
        return f'{self.user.username} Profile'
    
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to='static/img/')
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products", verbose_name="Магазин")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return f"{self.name} ({self.price})"
