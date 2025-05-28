from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.forms import SignUpForm, ReviewForm
from .models import Product, ProductCategory, Review
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    cart.add(product=product, quantity=quantity)
    return redirect('cart')


@login_required
def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': list(cart), 'total_price': cart.get_total_price()})


@login_required
def remove_from_cart(request, cart_id):
    cart = Cart(request)
    cart.remove(str(cart_id))
    return redirect('cart')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('catalog')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {'username': username})


def catalog_view(request):
    return product_list_view(request)


def product_list_view(request):
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    categories = ProductCategory.objects.all()
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'products': products, 'query': query})
