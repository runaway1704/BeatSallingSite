from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BeatListView.as_view(), name="beat_list"),
]