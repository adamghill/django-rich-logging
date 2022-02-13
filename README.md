<p align="center">
  <a href="https://django-rich-logging.readthedocs.io"><h1 align="center">django-rich-logging</h1></a>
</p>
<p align="center">A prettier way to see Django requests while developing.</p>

![PyPI](https://img.shields.io/pypi/v/django-rich-logging?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-rich-logging?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

📖 Complete documentation: https://django-rich-logging.readthedocs.io

📦 Package located at https://pypi.org/project/django-rich-logging/

## ⭐ Features

- live-updating table of all requests while developing

![demo of django-rich-logging](https://raw.githubusercontent.com/adamghill/django-rich-logging/main/django-rich-logging.gif)

## Installation

`poetry add django-rich-logging` OR `pip install django-rich-logging`

### Configuration

```python
# settings.py

# other settings here

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "django_rich_logging": {
            "class": "django_rich_logging.logging.DjangoRequestHandler",
            "level": "INFO",
        },
    },
    "loggers": {
        "django.server": {"handlers": ["django_rich_logging"], "level": "INFO"},
    },
}

# other settings here
```

Read all of the documentation at https://django-rich-logging.readthedocs.io.
