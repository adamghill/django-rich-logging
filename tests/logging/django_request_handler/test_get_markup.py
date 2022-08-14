import logging
from datetime import datetime

import pytest

from django_rich_logging.logging import DjangoRequestHandler
from django_rich_logging.objects import RequestRecord


@pytest.fixture
def handler():
    handler = DjangoRequestHandler()

    assert handler.live is not None
    assert handler.table is not None
    assert len(handler.table.rows) == 0

    return handler


@pytest.fixture
def request_record():
    log_record = logging.LogRecord(
        "django.server",
        logging.INFO,
        pathname="path",
        lineno=1,
        msg='"GET /profile HTTP/1.1" 200 1234',
        args=("GET /profile HTTP/1.1", "200", "1234"),
        exc_info=None,
    )

    request_record = RequestRecord(log_record)

    setattr(request_record, "created", datetime(2022, 8, 14, 19, 8, 1, 2))

    return request_record


def test_get_markup_no_style(handler, request_record):
    column = {"format": "[white]%(method)s"}

    expected = "[white]GET"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_percentage_style(handler, request_record):
    column = {"format": "[white]%(method)s", "style": "%"}

    expected = "[white]GET"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_bracket_curly_style(handler, request_record):
    column = {"format": "[white]{method}", "style": "{"}

    expected = "[white]GET"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_dollar_style(handler, request_record):
    column = {"format": "[white]$method", "style": "$"}

    expected = "[white]GET"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_method(handler, request_record):
    column = {"format": "{method}", "style": "{"}

    expected = "GET"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_status_code(handler, request_record):
    column = {"format": "{status_code}", "style": "{"}

    expected = "200"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_path(handler, request_record):
    column = {"format": "{path}", "style": "{"}

    expected = "/profile"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_created(handler, request_record):
    column = {"format": "{created}", "style": "{"}

    expected = "2022-08-14 19:08:01.000002"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_size(handler, request_record):
    column = {"format": "{size}", "style": "{"}

    expected = "1234"
    actual = handler._get_markup(request_record, column)

    assert expected == actual


def test_get_markup_invalid_style(handler, request_record):
    column = {"format": "{size}", "style": "x"}

    with pytest.raises(Exception):
        handler._get_markup(request_record, column)
