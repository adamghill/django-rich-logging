import logging

import pytest

from django_rich_logging.logging import DjangoRequestHandler


@pytest.fixture
def log_record():
    return logging.LogRecord(
        "django.server",
        logging.INFO,
        pathname="path",
        lineno=1,
        msg='"GET /profile HTTP/1.1" 200 1234',
        args=("GET /profile HTTP/1.1", "200", "1234"),
        exc_info=None,
    )


@pytest.fixture
def handler():
    handler = DjangoRequestHandler()

    assert handler.live is not None
    assert handler.uri_table is not None
    assert len(handler.uri_table.rows) == 0

    return handler


def _get_cell(handler, column_idx, row_idx):
    return list(
        handler.uri_table._get_cells(
            handler.console, 0, handler.uri_table.columns[column_idx]
        )
    )[row_idx]


def test_emit(handler, log_record):
    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1


def test_emit_non_django_server_log_record(handler, log_record):
    log_record.name = "not-django.server"

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 0


def test_emit_log_record_with_not_3_args(handler, log_record):
    log_record.args = ("127.0.0.1", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 0


def test_emit_200(handler, log_record):
    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1

    cell = _get_cell(handler, column_idx=0, row_idx=1)
    text = cell.renderable.renderable

    assert str(text) == "GET"
    assert text.style == "green"


def test_emit_301(handler, log_record):
    log_record.args = ("GET /profile HTTP/1.1", "301", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1

    cell = _get_cell(handler, column_idx=0, row_idx=1)
    text = cell.renderable.renderable

    assert str(text) == "GET"
    assert text.style == "yellow"


def test_emit_404(handler, log_record):
    log_record.args = ("GET /profile HTTP/1.1", "404", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1

    cell = _get_cell(handler, column_idx=0, row_idx=1)
    text = cell.renderable.renderable

    assert str(text) == "GET"
    assert text.style == "yellow"


def test_emit_500(handler, log_record):
    log_record.args = ("GET /profile HTTP/1.1", "500", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1

    cell = _get_cell(handler, column_idx=0, row_idx=1)
    text = cell.renderable.renderable

    assert str(text) == "GET"
    assert text.style == "red"


def test_emit_skip_favicon(handler, log_record):
    log_record.args = ("GET /favicon.ico HTTP/1.1", "200", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 0


def test_emit_no_matches(handler, log_record):
    log_record.args = ("this will not match the regex", "500", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 0


def test_emit_static_url(settings, handler, log_record):
    settings.STATIC_URL = "/static/"
    log_record.args = ("GET /static/vue.js HTTP/1.1", "200", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 0


def test_emit_static_url_setting_is_different(settings, handler, log_record):
    settings.STATIC_URL = "/static2/"
    log_record.args = ("GET /static/vue.js HTTP/1.1", "200", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1


def test_emit_missing_static_setting(settings, handler, log_record):
    settings.STATIC_URL = None
    log_record.args = ("GET /static/vue.js HTTP/1.1", "200", "1234")

    handler.emit(log_record)

    assert len(handler.uri_table.rows) == 1
