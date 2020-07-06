from .models import OrderItem, Order
from django.core.mail import send_mail, EmailMessage


def send_beat(order_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    subject = f"Заказ номер {order_id}"
    message = f"""Здравствуйте, {order.first_name}, ваш заказ номер {order_id}.
Ваш заказ(ы) - """
    file_path = []
    for item in order_item:
        name = item.beat.name
        file = item.beat.file.path
        message += f"{name}, "
        file_path.append(file)
    email = EmailMessage(subject, message, "workqpay@gmail.com", [order.email])
    for index in range(0, len(file_path)):
        email.attach_file(file_path[index])
    email.send(fail_silently=False)