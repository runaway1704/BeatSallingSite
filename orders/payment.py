from liqpay.liqpay3 import LiqPay
from django.conf import settings


def pay(total_price, order_id):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    params = {
        'action': 'pay',
        'amount': f'{total_price}',
        'currency': 'USD',
        'description': 'Payment for beat',
        'order_id': f'{order_id}',
        'version': '3',
        # 'server_url': 'https://test.com/billing/pay-callback/',  # url to callback view
    }
    # data = liqpay.cnb_data(params)
    # signature = liqpay.cnb_signature(params)
    html = liqpay.cnb_form(params)
    return html  # data, signature
