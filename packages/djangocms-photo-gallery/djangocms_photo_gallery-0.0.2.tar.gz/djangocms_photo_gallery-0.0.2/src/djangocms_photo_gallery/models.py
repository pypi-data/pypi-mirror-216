from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext as _
from djangocms_text_ckeditor.fields import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField
from parler.models import TranslatableModel, TranslatedFields


class Album(TranslatableModel):
    translations = TranslatedFields(
        name=models
        .CharField(blank=True, max_length=100, verbose_name=_('name of album'))
    )

    class Meta:
        verbose_name: str = _('album')
        verbose_name_plural: str = _('albums')

    def __str__(self):
        return self.name or _('– no name –')


class AlbumPicture(TranslatableModel):
    """Album picture with caption and copyright notice"""
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, verbose_name=_('album')
    )
    picture = ThumbnailerImageField(
        upload_to='djangocms_photo_gallery', verbose_name=_('picture')
    )
    translations = TranslatedFields(
        title=models.CharField(
            blank=True, max_length=50, verbose_name=_('title')
        ),
        caption=HTMLField(blank=True, verbose_name=_('caption')),
        copyright_notice=models.CharField(
            blank=True, max_length=50, verbose_name=_('copyright notice')
        )
    )

    class Meta:
        verbose_name: str = _('album picture')
        verbose_name_plural: str = _('album pictures')

    def __str__(self):
        return f'{self.caption}'


class AlbumPlugin(CMSPlugin):
    album = models.ForeignKey(
        Album, verbose_name=_('album'), on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.album.name}'
