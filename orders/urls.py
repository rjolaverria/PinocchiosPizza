from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order", views.order, name="order"),
    path("orders_info", views.orders_info, name="orders_info"),
    path("order/<category>", views.order_category, name="order_category"),
    path("signin", views.signin_view, name="signin"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("add_item", views.add_item, name="add"),
    path("remove_item/<item_id>", views.remove_item, name="remove"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout")
]
