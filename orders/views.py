from django.shortcuts import render
from django.conf import settings
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem, Order
from .tasks import send_beat
from django.views.decorators.http import require_http_methods
from liqpay.liqpay3 import LiqPay


@require_http_methods(["GET", "POST"])
def create_order(request):
    cart = Cart(request)
    total = cart.get_total_price()
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(beat=item["beat"],
                                         price=item["price"],
                                         order=order)
            # cart.clear()
            # send_beat(order.id)
            # Order.objects.filter(id=order.id).update(paid=True)
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            params = {'action': 'pay',
                      'amount': f'{total}',
                      'currency': 'USD',
                      'description': 'Payment for beat',
                      'order_id': f'{order.id}',
                      'version': '3'}
            html = liqpay.cnb_form(params=params)
            pay_order(request, cart, order.id)
            return render(request, "orders/order/created.html", {
                "order": order,
                "cart": cart,
                "html": html})
    else:
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})


def pay_order(request, cart, order_id):
    cart = cart
    send_beat(order_id)
    cart.clear()
    return
