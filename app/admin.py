from django.contrib import admin
from .models import Product, ProductCategory, Review, Notification
from django.contrib.auth.models import User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'category', 'views', 'orders_count', 'created_at')
    search_fields = ('name', 'description', 'seller__username')
    list_filter = ('category', 'created_at')
    readonly_fields = ('views', 'orders_count', 'created_at')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'text')
    list_filter = ('rating', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    list_filter = ('type', 'is_read', 'created_at')

admin.register(User)