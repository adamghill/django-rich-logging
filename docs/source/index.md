# Introduction

`django-rich-logging` outputs the current request in a live updating table for easy parsing.

## Installation

`poetry add django-rich-logging` OR `pip install django-rich-logging`

### Configuration

Configuring logging in Django (and in Python in general) can sometimes be a little obtuse. `django-rich-logging` uses the log records emitted by the `django.server` logger to do its magic.

**Minimal example configuration**

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
        "django.request": {"level": "CRITICAL"},
    },
}

# other settings here
```

The important parts are:

- listen to the `django.server` logger
  - the level must be `INFO` or below get all requests
  - there must be a handler which uses `django_rich_logging.logging.DjangoRequestHandler`
- `django.request` should be set to `CRITICAL` otherwise you will see 4xx and 5xx status codes getting logged twice

## More information about Django logging

- Information about logging `django.server`: https://docs.djangoproject.com/en/stable/ref/logging/#django-server
- Generic information about logging with Django: https://docs.djangoproject.com/en/stable/topics/logging/

## Other logging approaches

- https://www.willmcgugan.com/blog/tech/post/richer-django-logging/
- [Django logging with Rich gist](https://gist.github.com/adamchainz/efd465f267ad048b04cdd2056058c4bd)

## Inspiration and thanks

- https://twitter.com/marcelpociot/status/1491771828091695111 for the initial inspiration and my reaction: https://twitter.com/adamghill/status/1491780864447033348

### Dependencies

- https://github.com/Textualize/rich for making terminal output beautiful

```{toctree}
:maxdepth: 2
:hidden:

self
```

```{toctree}
:maxdepth: 2
:hidden:

GitHub <https://github.com/adamghill/django-rich-logging>
Sponsor <https://github.com/sponsors/adamghill>
```
