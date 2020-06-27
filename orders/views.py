from django.shortcuts import render
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem
from .tasks import send_beat


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
            send_beat(order.id)
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})
