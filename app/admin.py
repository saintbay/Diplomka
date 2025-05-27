from django.contrib import admin
from .models import Product, ProductCategory
from django.contrib.auth.models import User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price', 'category', 'created_at', 'updated_at') 
    search_fields = ('name', 'category__name')  
    list_filter = ('category',)  
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',) 
admin.register(User)