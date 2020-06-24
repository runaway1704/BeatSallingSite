from django.shortcuts import render
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem


def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(beat=item["beat"],
                                         price=item["price"],
                                         order=order)
            cart.clear()
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})
