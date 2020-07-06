from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("pay/<str:order_id>", views.pay, name="pay"),
    path("pay/callback", views.PayCallbackView.as_view, name="pay-callback")
]