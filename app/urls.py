from django.urls import path, include
from .views import (
    catalog_view, product_detail, cart_view, profile_view,
    remove_from_cart, search_view, signup_view, login_view,
    logout_view, home, add_to_cart, create_product, my_products,
    edit_product, delete_product, notifications, mark_notification_read,
    get_notification_count, about, add_review, checkout, order_success,
    my_orders, update_cart_quantity, mark_all_notifications_read,
    order_detail, confirm_order, support_home,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('about/', about, name='about'),
    path('catalog/', catalog_view, name='catalog'),
    path('search/', search_view, name='search'),

    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('create_product/', create_product, name='create_product'),
    path('my_products/', my_products, name='my_products'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),

    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart_quantity, name='update_cart_quantity'),

    path('checkout/', checkout, name='checkout'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('order/<int:order_id>/confirm/', confirm_order, name='confirm_order'),

    path('profile/', profile_view, name='profile'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('get_notification_count/', get_notification_count, name='get_notification_count'),

    path('support/', support_home, name='support_home'),
] 