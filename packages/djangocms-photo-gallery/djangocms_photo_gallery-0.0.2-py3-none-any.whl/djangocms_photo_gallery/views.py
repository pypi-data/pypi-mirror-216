from django.views.generic import ListView

from .models import Album


class GalleryListView(ListView):
    model = Album
