from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('profile/', views.profile_view, name='profile'),
    path('seller/<int:seller_id>/', views.seller_profile, name='seller_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('get-notification-count/', views.get_notification_count, name='get_notification_count'),
    path('create-product/', views.create_product, name='create_product'),
    path('my-products/', views.my_products, name='my_products'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
    path('support/', views.support_home, name='support_home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

