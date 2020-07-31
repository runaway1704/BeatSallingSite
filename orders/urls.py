from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("pay/", views.pay, name="pay"),
    path("callback/", views.PayCallbackView.as_view(), name="pay-callback"),
]