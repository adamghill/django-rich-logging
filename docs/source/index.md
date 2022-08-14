# Introduction

`django-rich-logging` outputs the current Django request in a live updating table for easy parsing.

## Installation

`poetry add django-rich-logging` OR `pip install django-rich-logging`

### Configuration

`django-rich-logging` uses the log records emitted by the `django.server` logger to do its magic. However, configuring logging in Django (and in Python in general) can sometimes be a little obtuse.

#### Minimal configuration

```python
# settings.py

# other settings here

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "django_rich_logging": {
            "class": "django_rich_logging.logging.DjangoRequestHandler",
        },
    },
    "loggers": {
        "django.server": {"handlers": ["django_rich_logging"]},
        "django.request": {"level": "CRITICAL"},
    },
}

# other settings here
```

- `DjangoRequestHandler` handles log messages from the `django.server` logger
  - the level must be `INFO` or below to get all requests (which it is by default)
  - there must be a handler which uses `django_rich_logging.logging.DjangoRequestHandler`
- `django.request` should be set to `CRITICAL` otherwise you will see 4xx and 5xx status codes getting logged twice

#### Only logging when debug

Most of the time, you will only want this type of logging when in local development (i.e. `DEBUG = True`). The `require_debug_true` logging filter can be used for this purpose.

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "django_rich_logging": {
            "class": "django_rich_logging.logging.DjangoRequestHandler",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django.server": {"handlers": ["django_rich_logging"]},
        "django.request": {"level": "CRITICAL"},
    },
}
```

#### Column configuration

The columns that are logged are configurable via the `columns` key in the `django_rich_logging` handler. The default column configuration is as follows.

```python
...
"handlers": {
    "django_rich_logging": {
        "class": "django_rich_logging.logging.DjangoRequestHandler",
        "columns": [
            {"header": "Method", "format": "[white]{method}", "style": "{"},
            {"header": "Path", "format": "[white bold]{path}", "style": "{"},
            {"header": "Status", "format": "{status_code}", "style": "{"},
            {"header": "Size", "format": "[white]{size}", "style": "{"},
            {
                "header": "Time",
                "format": "[white]{created}",
                "style": "{",
                "datefmt": "%H:%M:%S",
            },
        ],
    },
},
...
```

- `header` is the name of the column header
- `format` follows the same conventions as a normal [Python logging formatter](https://docs.python.org/3/howto/logging.html#formatters) which uses string interpolation to insert data from the current request
- [Similar to a logging formatter](https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles), `style` can be specified for the type of string interpolation to use (e.g. `%`, `{`, or `$`); to follow legacy Python conventions, `style` defaults to `%`

The available information that be specified in `format`:
- `method`: HTTP method, e.g. _GET_, _POST_
- `path`: The path of the request, e.g. _/index_
- `status_code`: Status code of the request, e.g. _200_, _404_, _500_
- `size`: Length of the content
- `created`: `datetime` of when the log was generated; can be additionally formatted into a string with `datefmt`

Formatted output can be colored or styled with the use of `rich` markup, e.g. `[white bold]something here[\white bold]`
- [`rich` markup syntax](https://rich.readthedocs.io/en/stable/markup.html#syntax)
- [Style attributes](https://rich.readthedocs.io/en/stable/style.html#styles), e.g. _bold_, _italic_
- [Available colors](https://rich.readthedocs.io/en/stable/appendix/colors.html), e.g. _red_, _blue_
- [Emojis](https://rich.readthedocs.io/en/stable/markup.html#emoji), e.g. _:warning:_

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
