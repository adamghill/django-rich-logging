import logging

from django_rich_logging.logging import DjangoRequestHandler
from rich.console import Console


def test_init_with_console():
    console = Console()
    handler = DjangoRequestHandler(console=console)

    assert id(console) == id(handler.console)


def test_init_with_no_console():
    handler = DjangoRequestHandler()

    assert handler.console is not None


def test_init_with_formatter():
    formatter = logging.Formatter(datefmt="%Y-%m-%d %H:%M:%S")
    handler = DjangoRequestHandler(formatter=formatter)

    assert id(formatter) == id(handler.formatter)


def test_init_with_no_formatter():
    handler = DjangoRequestHandler()

    assert handler.formatter is not None


def test_init_with_live():
    handler = DjangoRequestHandler()

    original_live_id = id(handler.live)

    handler.__init__()
    assert original_live_id == id(handler.live)
