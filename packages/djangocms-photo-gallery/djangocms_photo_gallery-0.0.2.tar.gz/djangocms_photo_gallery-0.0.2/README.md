# djangocms-photo-gallery

[![PyPI - Version](https://img.shields.io/pypi/v/djangocms-photo-gallery.svg)](https://pypi.org/project/djangocms-photo-gallery)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/djangocms-photo-gallery.svg)](https://pypi.org/project/djangocms-photo-gallery)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install djangocms-photo-gallery
```

Settings:

```python
INSTALLED_APPS: list[str] = [
    # …
    'easy_thumbnails',
    'djangocms_photo_gallery',
]

THUMBNAIL_ALIASES: dict[str, dict[str, dict[str, any]]] = {
    # …
    'djangocms_photo_gallery':
        {
            'overview': {
                'size': (300, 200),
                'crop': 'smart',
                'upscale': True
            },
            'popup':
                {
                    'size': (1400, 1400),
                    'crop': False,
                    'upscale': False
                },
        },
}
```
The following CSS and JS libraries should be included in you base template, which should be named
`base.html`:

* [jQuery](https://jquery.com/)
* [Fomantic-UI](https://fomantic-ui.com/)
* [Colorbox - a jQuery lightbox](https://www.jacklmoore.com/colorbox/)

Alternatively you can change the templates and use libraries of your choice.

## License

`djangocms-photo-gallery` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
