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

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to='static/img/')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.price})"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Отзыв")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f'Отзыв от {self.user.username} для {self.product.name}'
