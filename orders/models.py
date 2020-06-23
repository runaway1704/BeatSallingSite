from django.db import models

from Beat.models import Beat


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ номер {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="Предметы", on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, related_name="Бит", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.id)

