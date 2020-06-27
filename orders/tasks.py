from .models import OrderItem, Order
from django.core.mail import send_mail, EmailMessage


def send_beat(order_id):
    order = Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)
    subject = f"Заказ номер{order_id}"
    message = ""
    file_path = ""
    for item in order_item:
        name = item.beat.name
        file = item.beat.file.path
        message += f"{name} \n"
        file_path += file
        yield file_path
    email = EmailMessage(subject, message, "fred@example.com", [order.email])
    for _ in range(1, order_item.count() + 1):  # отправлять файлов столько сколько попадает в order_item
        email.attach_file(file_path)
    # email.attach_file(file_path)
    email.send(fail_silently=False)

    # mail_sent = send_mail(subject,
    #                       message,
    #                       "andreypoelsup@gmail.com",
    #                       [order.email],
    #                       )
    # return mail_sent
