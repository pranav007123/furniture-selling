from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse



def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'home.html', context)

# View for listing products within a specific category
def products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'products.html', context)

# View for product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})



# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')


# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')



# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully! You can log in now.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'register.html')




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create a cart item for the product
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Set quantity to 1 if new, otherwise increase by 1
    if item_created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('view_cart')




# View to display the cart and its items
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


# View to update the quantity of an item in the cart
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        action = request.POST.get('action')

        # Increase or decrease quantity based on action
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        # Save or delete based on updated quantity
        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('view_cart')



# View to remove an item from the cart
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)



@login_required

def process_order(request):
    if request.method == "POST":
        print("Process Order view is being called")  # Debugging line

        # Retrieve form data
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        payment_method = request.POST.get('payment_method')

        # Calculate total amount based on cart items
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_amount = sum(item.get_total_price() for item in cart_items)

        # Create the Order entry
        order = Order.objects.create(
            user=request.user,
            address=address,
            city=city,
            zip_code=zip_code,
            phone_number=phone_number,
            email=email,
            payment_method=payment_method,
            total_amount=total_amount,
            status='Pending'
        )

        # Create OrderItem entries for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Reduce stock for the ordered products
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart after order placement
        cart.items.all().delete()

        # Notify user and redirect to the success page
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

    # Redirect to checkout if the request method is not POST
    return redirect('checkout')


@login_required
def order_summary(request):
    # Get the latest order for the user
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()

    if not order:
        messages.info(request, "You have no recent orders.")
        return redirect('home')

    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'order_summary.html', context)



@login_required
def order_success(request):

    return render(request, 'order_success.html')


def user_orders(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_orders.html', {'orders': orders})