from django.contrib import admin
from .models import Product, ProductCategory
from django.contrib.auth.models import User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price', 'category', 'created_at', 'updated_at')  # что отображать в списке товаров
    search_fields = ('name', 'category__name')  # поля для поиска
    list_filter = ('category',)  # фильтры по категориям
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # что отображать в списке категорий
    search_fields = ('name',)  # поля для поиска
admin.register(User)