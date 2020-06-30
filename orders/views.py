from django.shortcuts import render
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem
from .tasks import send_beat
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def create_order(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            total_price = 0
            for item in cart:
                total_price += item["price"]
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
