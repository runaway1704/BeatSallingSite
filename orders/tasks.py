from .models import OrderItem, Order
from django.core.mail import send_mail, EmailMessage


def send_beat(order_id):  # отправляет бит по почте
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    subject = f"Заказ номер {order_id}"
    message = f"""Здравствуйте, {order.first_name}, ваш заказ номер {order_id}.
Ваш заказ(ы) - """
    for item in order_item:
        name = item.beat.name
        file = item.beat.url_to_cloud
        message += f"{name} - {file},\n "
    email = EmailMessage(subject, message, "andreylukyanchuk623@gmail.com", [order.email])  # workqpay@gmail.com
    email.send(fail_silently=False)