from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View, TemplateView

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
            # pay_order(request, cart, order.id)
            return render(request, "orders/order/order_page.html", {
                "order": order,
                "cart": cart})
    else:
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})


def pay(request, order_id):
    cart = Cart(request)
    total = cart.get_total_price()
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'pay',
        'amount': f'{total}',
        'currency': 'UAH',
        'description': 'Payment for clothes',
        'order_id': f'{order_id}',
        'version': '3',
        'sandbox': 1,  # sandbox mode, set to 1 to enable it
        'server_url': f'# https://extorfinbeat.herokuapp.com/orders/callback/{order_id}',  # url to callback view
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    return render(request, "orders/order/pay.html", {'signature': signature, 'data': data,
                                                     'order_id': str(order_id)})


@method_decorator(csrf_exempt, name='dispatch')
def callback(request):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    data = request.POST.get('data')
    signature = request.POST.get('signature')
    print(signature)
    i_d = request.POST.get("order_id")
    print(i_d)
    # sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
    # if sign == signature:
    #
    #     print('CALLBACK IS VALID!')
    # response = liqpay.decode_data_from_str(data)
    # print(response)
    return HttpResponse()
#