from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View, TemplateView

from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem, Order
from .tasks import send_beat
from liqpay.liqpay3 import LiqPay

order_id = 0  # номер заказа вынес сюда, т.к. надо его использовать во всех вьюхах


def create_order(request):
    """создание заказа"""
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(beat=item["beat"],
                                         price=item["price"],
                                         order=order)
            global order_id
            order_id = order.id
            # cart.clear()
            # send_beat(order.id)
            # Order.objects.filter(id=order.id).update(paid=True)
            return render(request, "orders/order/order_page.html", {
                "order": order,
                "cart": cart})
    else:
        form = OrderCreateForm
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})


def pay(request):
    """переадресация на оплату"""
    if order_id == 0:
        return redirect("beat_list")
    else:
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
            # 'server_url': 'https://extorfinbeat.herokuapp.com/en/orders/callback/',  # url to callback view
            'server_url': 'http://127.0.0.1:8000/en/orders/callback',
            "result_url": 'http://127.0.0.1:8000/en/orders/callback'
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, "orders/order/pay.html", {'signature': signature, 'data': data,
                                                         'order_id': str(order_id)})


# @method_decorator(csrf_exempt, name='dispatch')
# def callback(request):
#     """нужна для отправки почты после оплаты"""
#     if order_id == 0:
#         return redirect("beat_list")
#     else:
#         cart = Cart(request)
#         liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
#         data = request.POST.get('data')
#         signature = request.POST.get('signature')
#         print(data, signature)
# sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
# if sign == signature:
# if signature and data is not None:
# cart.clear()
# send_beat(order_id)
# Order.objects.filter(id=order_id).update(paid=True)
# response = liqpay.decode_data_from_str(data)
# print(response)
# return redirect("beat_list")
@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        if order_id == 0:
            return redirect("beat_list")
        else:
            cart = Cart(request)
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            data = request.POST.get('data')
            signature = request.POST.get('signature')
            # if data and signature:
            cart.clear()
            send_beat(order_id)
            Order.objects.filter(id=order_id).update(paid=True)
            # sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
            # if sign == signature:
            #     print('callback is valid')
            return redirect("beat_list")

    def get(self, request, *args, **kwargs):

        if order_id == 0:
            return redirect("beat_list")
        else:
            cart = Cart(request)
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            data = request.GET.get('data')
            signature = request.GET.get('signature')
            # print(data, signature)
            cart.clear()
            send_beat(order_id)
            Order.objects.filter(id=order_id).update(paid=True)
            # sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
            # if sign == signature:
            #     print('callback is valid')
        return redirect("beat_list")
