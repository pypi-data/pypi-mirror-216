from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _


@apphook_pool.register
class DjangocmsGalleryApphook(CMSApp):
    app_name: str = 'djangocms_photo_gallery'
    name: str = _('django CMS Photo Gallery')

    def get_urls(self, page=None, language=None, **kwargs) -> list:
        return ['djangocms_photo_gallery.urls']
