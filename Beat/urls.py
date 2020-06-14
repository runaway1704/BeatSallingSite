from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BeatListView.as_view(), name="beat_list"),
    path('beat/<slug:slug>', views.BeatDetailView.as_view(), name="beat_detail")
]