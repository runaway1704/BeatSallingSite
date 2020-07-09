from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("pay/<str:order_id>", views.pay, name="pay"),
    path("callback/", views.callback, name="pay-callback"),
    # path("test/", views.test, name='test')
]