from pathlib import Path

from django.conf import settings


def pytest_configure():
    base_dir = Path(".")

    settings.configure(
        BASE_DIR=base_dir,
        SECRET_KEY="this-is-a-secret",
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": ["tests/templates"],
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                    ],
                },
            }
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {},
            "handlers": {
                "django_rich_logging": {
                    "class": "django_rich_logging.logging.DjangoRequestHandler",
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "django.server": {
                    "handlers": ["django_rich_logging"],
                    "level": "INFO",
                },
            },
        },
    )
