from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Beat


class BeatListView(ListView):
     model = Beat
     queryset = Beat.objects.all()
     # template_name = "Pages/beat_list_view.html"


class MovieDetailView(DetailView):  # даёт возможность для movie_detail.html использовать movie
    """detail view to films"""
    model = Beat
    slug_field = "url"
    # template_name = "Pages/beat_detail.html"