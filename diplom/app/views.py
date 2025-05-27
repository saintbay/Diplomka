from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.forms import SignUpForm
from .models import Product, ProductCategory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import pprint
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product  
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, quantity=quantity)

    return redirect(reverse('cart'))

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})
    


@login_required
def remove_from_cart(request, cart_id):
    print(f"Removing product with ID: {cart_id}")  
    cart = Cart(request)
    cart.remove(product_id=str(cart_id)) 
    print("Cart contents after removal:", cart.cart)  
    return redirect('cart')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {'username': username})
def catalog_view(request):
    products = Product.objects.all() 
    return render(request, 'catalog.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id) 
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart_view(request):
    return render(request, 'cart.html')
@login_required
def profile_view(request):
    return render(request, 'profile.html')

def search_view(request):
    query = request.GET.get('q', '')  
    products = Product.objects.filter(name__icontains=query)  
    return render(request, 'search_results.html', {'products': products, 'query': query})

