from rich.console import Console

from django_rich_logging.logging import DjangoRequestHandler


def test_init_with_console():
    console = Console()
    handler = DjangoRequestHandler(console=console)

    assert id(console) == id(handler.console)


def test_init_with_no_console():
    handler = DjangoRequestHandler()

    assert handler.console is not None


def test_init_with_live():
    handler = DjangoRequestHandler()

    original_live_id = id(handler.live)

    handler.__init__()
    assert original_live_id == id(handler.live)
