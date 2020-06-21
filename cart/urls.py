from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:beat_id>", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:beat_id>", views.remove_from_cart, name="remove_from_cart"),
]