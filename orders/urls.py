from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("pay/", views.pay_order, name="pay")
]