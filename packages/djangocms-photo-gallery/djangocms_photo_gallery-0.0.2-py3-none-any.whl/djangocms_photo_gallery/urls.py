from django.urls import path

from . import views

app_name = 'djangocms_photo_gallery'
urlpatterns = [
    path('', views.GalleryListView.as_view(), name='gallery'),
]
