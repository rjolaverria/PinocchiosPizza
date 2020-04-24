from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

import json

from .models import MenuItem, Topping, Order, Order_item

# Create your views here.
context = {
    "menu": MenuItem.objects.all(),
    "menu_cats": MenuItem.objects.order_by().values('category').distinct(),
    "toppings": Topping.objects.all()
}

# Order helper


def validate_order(request):
    if request.user.is_authenticated:
        order = None
        try:
            order = Order.objects.filter(
                user_id=request.user.id).get(checked_out=False)
        except Order.DoesNotExist:
            order = Order(user=request.user)
            order.save()
        return order
    else:
        return False


def index(request):
    order = validate_order(request)
    if order:
        return HttpResponseRedirect(reverse('order'))
    return render(request, "orders/index.html", {**context, 'order': order})


def order(request):
    order = validate_order(request)
    return render(request, "orders/order.html", {**context, 'order': order})


def order_category(request, category):
    # Check if user is logged in
    if request.user.is_authenticated:

        # Current Order
        order = validate_order(request)

        # Add menu items to list
        items = []
        for item in context['menu']:
            if item.category == category:
                items.append(item)

        # Return to order page if category does not exist
        if len(items) < 1:
            return HttpResponseRedirect(reverse(order))

        # Render page with items for category
        return render(request, "orders/order-item.html", {'category': category, 'items': items, "toppings": context["toppings"], 'order': order})

    # Return to order page if not logged in
    return HttpResponseRedirect(reverse(order))


def register(request):
    # redirect if signed in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('order'))

    # Check if form is submitted
    if request.method == 'POST':

        # Create form
        form = UserCreationForm(request.POST)

        # Check form Validity
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('order'))
    else:
        form = UserCreationForm()

    # Render form page
    return render(request, 'orders/register.html', {'form': form})


def signin_view(request):
    # Redirect is signed in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('order'))

    if request.method == 'POST':
        # Get username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check authenticity of user for redirection
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('order'))
        else:
            return render(request, 'orders/signin.html', {"error": "Invalid credentials."})
    return render(request, 'orders/signin.html')


def logout_view(request):
    logout(request)
    return render(request, "orders/index.html", context)


def add_item(request):
    # Get order
    order = validate_order(request)

    if order:
        # Order item details
        body = json.loads(request.body.decode('utf8'))
        item_id = int(body.get('itemId'))
        item = MenuItem.objects.get(pk=item_id)
        size = body.get('size')
        extras = body.get('extras')
        price = 0
        if size == 'large':
            price = float(item.large_price)
        else:
            price = float(item.price)
        if item.category == 'Sub':
            price += len(extras) * 0.50

        # Add item and check for error
        try:
            order_item = Order_item(order=order, item=item, size=size,
                                    extras=', '.join(extras), price=price)
            order.item_count += 1
            order.total = float(order.total) + order_item.price
            order_item.save()
            order.save()
            return HttpResponse(str(order.item_count))
        except ValueError:
            return HttpResponse("Error adding Item")
    return HttpResponseRedirect(reverse('order'))


def remove_item(request, item_id):
    if request.user.is_authenticated:
        try:
            item = Order_item.objects.get(pk=item_id)
            order = item.order
            order.item_count -= 1
            order.total -= item.price
            item.delete()
            order.save()
            return HttpResponseRedirect(reverse('cart'))
        except Order_item.DoesNotExist:
            HttpResponse("No Item exists"), 404
    return HttpResponseRedirect(reverse('index'))


def cart(request):
    order = validate_order(request)
    if order:
        order_items = Order_item.objects.filter(order=order)
        return render(request, "orders/cart.html", {'order': order, 'order_items': order_items})


def orders_info(request):
    order = validate_order(request)
    if request.user.is_authenticated:
        orders = Order.objects.filter(
            user=request.user).order_by('-check_out_date')
        items = Order_item.objects.all()
        return render(request, "orders/orders-info.html", {'orders': orders, 'items': items, 'order': order})


def checkout(request):
    order = validate_order(request)
    if order:
        order.checked_out = True
        order.check_out_date = timezone.localtime(timezone.now())
        print(order.check_out_date)
        order.save()
        return HttpResponseRedirect(reverse('orders_info'))

    return HttpResponseRedirect(reverse('order'))
