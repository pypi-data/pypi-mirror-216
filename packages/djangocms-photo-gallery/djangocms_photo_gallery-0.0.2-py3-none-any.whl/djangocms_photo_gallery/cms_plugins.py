from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext as _

from .models import AlbumPlugin


@plugin_pool.register_plugin
class DjangocmsAlbumPublisher(CMSPluginBase):
    model: CMSPlugin = AlbumPlugin
    module: str = _('djangocms_photo_gallery')
    name: str = _('django CMS Album')
    render_template: str = 'djangocms_photo_gallery/plugins/album.html'
