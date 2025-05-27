from django.contrib import admin
# from django.urls import path
# from app.views import home2,logout_view,product_detail_view,profile_view,cart_view,search_view ,login_view, register_view
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('home/', home2, name='home'),
#     # path('', SignUp.as_view(), name='class_signup'),
#     # path('manual_signup/', manual_signup, name='manual_signup'),
#     path('login/', login_view, name='login'),
#     path('signup/', register_view, name='signup'),
#     path('cart/',cart_view,name='cart'),
#     path('search/',search_view,name='search'),
#     path('private/',profile_view,name='profile'),
#     path('product/<int:product_id>/', product_detail_view, name='product_detail'),
#     path('logout/', logout_view, name='logout')
# ] 
from django.urls import path
from app.views import catalog_view, product_detail_view, cart_view, profile_view,remove_from_cart, search_view, signup_view, login_view, logout_view,home,add_to_cart
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('catalog/',catalog_view,name='catalog'),
    path('profile/', profile_view, name='profile'),
    path('search/', search_view, name='search'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)