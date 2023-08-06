# Photo gallery for django CMS

This gallery uses:

* [django CMS](https://www.django-cms.org/)
* [Django Sekizai](https://github.com/django-cms/django-sekizai)
* [jQuery](https://jquery.com/) is needed by Colorbox and Fomantic UI and should be included in the 
  base template `outphit.html`, which is not includded in this app.
* [Colorbox - a jQuery lightbox](https://www.jacklmoore.com/colorbox/) for overlay slide shows
  The files `js/colorbox/colorbox.css` and `js/colorbox/jquery.colorbox-min.js` are linked in
  `outphit_photo_gallery/templates/outphit_photo_gallery/include/album.html`
* [Fomantic UI](https://fomantic-ui.com/) Some HTML classes are used in the
  templates, mainly for the grid. They can easily be replaced by another framework or pure CSS.
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails) for scaling down the pictures
* [django-parler](https://github.com/django-parler/django-parler) for translatable fields
* [djangocms_text_ckeditor](https://github.com/django-cms/djangocms-text-ckeditor) for captions

In the settings of the project (e. g. `settings.py`), you need to add entries in ` 

```python
INSTALLED_APPS: list = [
    # …
    'easy_thumbnails',
    'djangocms_photo_gallery',
]

THUMBNAIL_ALIASES = {
    '': {
        'gallery': {
                    'size': (300, 200),
                    'crop': 'smart',
                    'upscale': True
                },
        },
}


```