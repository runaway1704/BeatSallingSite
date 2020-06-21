from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from .cart import Cart
from Beat.models import Beat


def add_to_cart(request, beat_id):
    cart = Cart(request)
    beat = get_object_or_404(Beat, id=beat_id)
    cart.add(beat=beat)
    return redirect("beat_list")


def remove_from_cart(request, beat_id):
    cart = Cart(request)
    beat = get_object_or_404(Beat, id=beat_id)
    cart.remove(beat=beat)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})
