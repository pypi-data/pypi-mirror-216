from django.contrib import admin
from django.utils.translation import gettext as _
from parler.admin import TranslatableAdmin, TranslatableStackedInline

from .models import Album, AlbumPicture


class GalleryPictureInline(TranslatableStackedInline):
    model = AlbumPicture
    extra = 5


@admin.register(Album)
class AlbumAdmin(TranslatableAdmin):
    verbose_name = _('album')
    verbose_name_plural = _('albums')
    inlines = [GalleryPictureInline]
