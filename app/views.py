from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.forms import SignUpForm,OrderForm
from .models import Product, ProductCategory, Review, Notification, Order, OrderItem, CartAddition
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .cart import Cart
from django.http import JsonResponse, HttpResponseForbidden
from .forms import ProductForm
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone


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
    if not request.user.is_authenticated:
        messages.warning(request, 'To add products to the cart, you need to log in to the system')
        return redirect('login')

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    
    CartAddition.objects.get_or_create(
        product=product,
        user=request.user
    )
    
    cart.add(product=product, quantity=quantity)

    Notification.objects.create(
        user=request.user,
        title='Product added to cart',
        message=f'You added the product "{product.name}" to the cart',
        type='purchase',
        link=reverse('cart')
    )

    if product.seller and product.seller != request.user:
        Notification.objects.create(
            user=product.seller,
            title='Product added to cart',
            message=f'User {request.user.username} added your product "{product.name}" to the cart',
            type='purchase',    
            link=reverse('product_detail', args=[product.id])
        )

    messages.success(request, f'Product "{product.name}" added to cart')
    return redirect('cart')


@login_required
def cart_view(request):
    cart = Cart(request)
    cart_items = list(cart)
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price()
    })


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(str(product_id))
    return redirect('cart')


@login_required
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        try:
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id)
            
            quantity_change = int(request.POST.get('quantity_change', 0))
            
            cart_item = cart.get_item(product_id)
            if cart_item is None:
                cart.add(product=product, quantity=1)
                cart_item = cart.get_item(product_id)
            
            current_quantity = cart_item['quantity']
            new_quantity = max(1, current_quantity + quantity_change)
            
            cart.add(product=product, quantity=new_quantity, update_quantity=True)
            
            total_price = cart.get_total_price()
            
            return JsonResponse({
                'success': True,
                'new_quantity': new_quantity,
                'total_price': str(total_price)
            })
            
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Product not found'
            })
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid value: {str(e)}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Server error: {str(e)}'
            })
            
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })


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
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    
    notifications_by_type = {
        'purchase': notifications.filter(type='purchase'),
        'review': notifications.filter(type='review'),
        'order': notifications.filter(type='order'),
    }
    
    unread_counts = {
        'purchase': notifications_by_type['purchase'].filter(is_read=False).count(),
        'review': notifications_by_type['review'].filter(is_read=False).count(),
        'order': notifications_by_type['order'].filter(is_read=False).count(),
    }

    notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
        'notifications_by_type': notifications_by_type,
        'unread_counts': unread_counts,
    }
    return render(request, 'notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        messages.success(request, 'Notification marked as read')
    return redirect('notifications')


@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        notification_type = request.POST.get('type')
        notifications = request.user.notifications.filter(is_read=False)
        
        if notification_type in ['purchase', 'review', 'order']:
            notifications = notifications.filter(type=notification_type)
            
        notifications.update(is_read=True)
        messages.success(request, 'All notifications marked as read')
    return redirect('notifications')


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product successfully added!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})


@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'my_products.html', {'products': products})


def get_notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


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
    product.views += 1
    product.save()
    
    reviews = product.reviews.all().order_by('-created_at')
    
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def seller_profile(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)
    products = Product.objects.filter(seller=seller)
    
    successful_sales = OrderItem.objects.filter(
        product__seller=seller,
        order__status__in=["delivered", "completed"]
    ).count()
    
    context = {
        'seller': seller,
        'products': products,
        'successful_sales': successful_sales,
        'total_products': products.count()
    }
    return render(request, 'seller_profile.html', context)


def search_view(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort')
    
    products = Product.objects.filter(name__icontains=query)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    categories = ProductCategory.objects.all()
    
    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
        'selected_sort': sort_by
    })


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.seller != request.user:
        return HttpResponseForbidden("You don't have permission to edit this product")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated!')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'create_product.html', {
        'form': form,
        'edit_mode': True,
        'product': product
    })


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.seller != request.user:
        return HttpResponseForbidden("You don't have permission to delete this product")
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product successfully deleted!')
        return redirect('my_products')
    
    return render(request, 'delete_product_confirm.html', {'product': product})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        if rating and text:
            actual_rating = 6 - int(rating)
            
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=actual_rating,
                text=text
            )

            Notification.objects.create(
                user=request.user,
                title='Review published',
                message=f'Your review about the product "{product.name}" has been successfully published',
                type='review',
                link=reverse('product_detail', args=[product.id])
            )
            if product.seller and product.seller != request.user:
                Notification.objects.create(
                    user=product.seller,
                    title='New review',
                    message=f'User {request.user.username} left a review about your product "{product.name}". Rating: {actual_rating} stars',
                    type='review',
                    link=reverse('product_detail', args=[product.id])
                )
            
            messages.success(request, 'Review successfully added!')
        
        return redirect('product_detail', product_id=product.id)
    
    return redirect('product_detail', product_id=product.id)


@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.get_total_price():
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = Decimal(cart.get_total_price())
            order.payment_confirmed = True
            order.payment_confirmed_at = timezone.now()
            order.save()

            sellers_notified = set()  
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                
                Notification.objects.create(
                    user=request.user,
                    title='Product purchased',
                    message=f'You bought the product "{item["product"].name}" in the amount of {item["quantity"]} pcs.',
                    type='order',
                    link=reverse('my_orders')
                )
                
                if item['product'].seller and item['product'].seller.id not in sellers_notified:
                    Notification.objects.create(
                        user=item['product'].seller,
                        title='New order',
                        message=f'User {request.user.username} bought your product "{item["product"].name}"',
                        type='order',
                        link=reverse('product_detail', args=[item['product'].id])
                    )
                    sellers_notified.add(item['product'].seller.id)

            cart.clear()

            messages.success(request, 'Order successfully placed!')
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm(initial={
            'phone': request.user.userprofile.phone if hasattr(request.user, 'userprofile') else ''
        })

    return render(request, 'checkout.html', {
        'form': form,
        'cart': cart
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    seller_orders = Order.objects.filter(
        items__product__seller=request.user
    ).distinct().order_by('-created_at')
    
    return render(request, 'my_orders.html', {
        'orders': orders,
        'seller_orders': seller_orders
    })


@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    is_seller = any(item.product.seller == request.user for item in order.items.all())
    is_buyer = order.user == request.user
    
    if not (is_seller or is_buyer):
        return HttpResponseForbidden("You don't have permission to confirm this order")
    
    if request.method == 'POST':
        action = request.POST.get('action', 'confirm')
        now = timezone.now()
        
        if is_seller and not order.seller_confirmed and action == 'confirm':
            order.seller_confirmed = True
            order.seller_confirmed_at = now
            order.payment_confirmed = True
            order.payment_confirmed_at = now
            order.save()
            order.update_status()
            
            Notification.objects.create(
                user=order.user,
                title='Order confirmed by seller',
                type='order',
                link=reverse('order_detail', args=[order.id])
            )
            
            messages.success(request, 'Order confirmed and will be sent!')
        
        elif is_buyer and not order.payment_confirmed and action == 'confirm_payment':
            order.payment_confirmed = True
            order.payment_confirmed_at = now
            order.save()
            
            sellers = set(item.product.seller for item in order.items.all() if item.product.seller)
            for seller in sellers:
                Notification.objects.create(
                    user=seller,
                    title='New paid order',
                    message=f'The buyer paid for the order #{order.id}. Please confirm the receipt of payment.',
                    type='order',
                    link=reverse('order_detail', args=[order.id])
                )
            
            messages.success(request, 'Payment confirmed!')
        
        elif is_buyer and order.seller_confirmed and not order.buyer_confirmed:
            if action == 'confirm':
                order.buyer_confirmed = True
                order.buyer_confirmed_at = now
                order.save()
                
                sellers = set(item.product.seller for item in order.items.all() if item.product.seller)
                for seller in sellers:
                    Notification.objects.create(
                        user=seller,
                        title='Order received',
                        message=f'The buyer confirmed the receipt of the order #{order.id}',
                        type='order',
                        link=reverse('order_detail', args=[order.id])
                    )
                
                messages.success(request, 'Order received confirmed!')
            
            elif action == 'not_received':
                order.status = 'not_received'
                order.save()
                
                sellers = set(item.product.seller for item in order.items.all() if item.product.seller)
                for seller in sellers:
                    Notification.objects.create(
                        user=seller,
                        title='Problem with the order',
                        message=f'The buyer reported that the order #{order.id} was not received',
                        type='order',
                        link=reverse('order_detail', args=[order.id])
                    )
                
                messages.warning(request, 'Order status changed to "Not received"')
        
        order.update_status()
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'confirm_order.html', {
        'order': order,
        'is_seller': is_seller,
        'is_buyer': is_buyer
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    sellers = set(item.product.seller for item in order.items.all() if item.product.seller)
    is_seller = request.user in sellers
    is_buyer = order.user == request.user
    
    if not (is_seller or is_buyer):
        return HttpResponseForbidden("You don't have permission to view this order")
    
    return render(request, 'order_detail.html', {
        'order': order,
        'is_seller': is_seller,
        'is_buyer': is_buyer
    })


@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        request.user.notifications.all().delete()
        messages.success(request, 'All notifications successfully deleted')
    return redirect('notifications')


def support_home(request):
    return render(request, 'support/home.html')




