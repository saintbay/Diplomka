from django.contrib import admin
from django.urls import path
from app.views import (
    catalog_view,product_detail , cart_view, profile_view,
    remove_from_cart, search_view, signup_view, login_view,
    logout_view, home, add_to_cart
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('admin/', admin.site.urls),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('catalog/', catalog_view, name='catalog'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('search/', search_view, name='search'),

    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),

    path('profile/', profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

