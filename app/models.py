from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    age = models.IntegerField(null=True, blank=True, verbose_name='Возраст')

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
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    image = CloudinaryField('image', folder='products', blank=True, null=True,
                          transformation={
                              'width': 800,
                              'height': 600,
                              'crop': 'fill',
                              'quality': 'auto',
                              'format': 'auto',
                          })
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    views = models.IntegerField(default=0)
    orders_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def unique_cart_additions(self):
        return self.cart_additions.count()

    @property
    def successful_orders_count(self):
        return self.orderitem_set.filter(order__status__in=["delivered", "completed"]).count()


class Review(BaseModel):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Отзыв")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")

    def __str__(self):
        return f'Отзыв от {self.user.username} для {self.product.name}'


class Notification(BaseModel):
    NOTIFICATION_TYPES = (
        ('purchase', 'Добавление в корзину'),
        ('review', 'Отзыв'),
        ('order', 'Покупка'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    link = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения оплаты'),
        ('paid', 'Оплачен'),
        ('seller_confirmed', 'Подтверждено продавцом'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
        ('not_received', 'Не получен')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField(verbose_name='Адрес доставки')
    phone = models.CharField(max_length=15, verbose_name='Телефон для связи')
    seller_confirmed = models.BooleanField(default=False, verbose_name='Подтверждено продавцом')
    buyer_confirmed = models.BooleanField(default=False, verbose_name='Подтверждено покупателем')
    seller_confirmed_at = models.DateTimeField(null=True, blank=True)
    buyer_confirmed_at = models.DateTimeField(null=True, blank=True)
    payment_confirmed = models.BooleanField(default=False, verbose_name='Оплата подтверждена')
    payment_confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def update_status(self):
        if not self.payment_confirmed:
            self.status = 'pending'
        elif self.payment_confirmed and not self.seller_confirmed:
            self.status = 'paid'
        elif self.seller_confirmed and not self.buyer_confirmed:
            self.status = 'seller_confirmed'
            if not self.status == 'not_received':
                self.status = 'shipped'
        elif self.buyer_confirmed:
            self.status = 'completed'
        elif self.status == 'not_received':
            pass
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.product.name} в заказе {self.order.id}'

    def get_total(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class CartAddition(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_additions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'user']

