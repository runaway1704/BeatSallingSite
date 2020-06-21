from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Beat


class BeatListView(ListView):
    model = Beat
    queryset = Beat.objects.all()
    template_name = "Beat/beat_list.html"
