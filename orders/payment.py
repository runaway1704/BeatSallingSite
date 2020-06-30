from liqpay.liqpay import LiqPay
from django.conf import settings


def pay(total_price, order_id):
    liqpay = LiqPay()
    params = {
        'action': 'pay',
        'amount': f'{total_price}',
        'currency': 'USD',
        'description': 'Payment for beat',
        'order_id': f'{order_id}',
        'version': '3',
        # 'server_url': 'https://test.com/billing/pay-callback/',  # url to callback view
    }
    html = liqpay.cnb_form(params=params)
    return html
