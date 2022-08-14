import logging

import pytest

from django_rich_logging.objects import RequestRecord


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


def test_request_record_is_valid(log_record):
    request_record = RequestRecord(log_record)

    assert request_record.is_valid


def test_request_record_arg0_is_invalid(log_record):
    log_record.args = ("blob", "200", "1234")
    request_record = RequestRecord(log_record)

    assert not request_record.is_valid


def test_request_record_missing_arg_is_invalid(log_record):
    log_record.args = ("GET /profile HTTP/1.1", "200")
    request_record = RequestRecord(log_record)

    assert not request_record.is_valid
