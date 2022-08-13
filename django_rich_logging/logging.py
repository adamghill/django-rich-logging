import logging

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

from .objects import Request


class DjangoRequestHandler(logging.StreamHandler):
    """
    A logging handler that prints Django requests in a live-updating table.
    """

    live = None
    uri_table = None
    console = None

    def __init__(self, *args, **kwargs):
        super().__init__()

        formatter = logging.Formatter(datefmt="%H:%M:%S")

        if "formatter" in kwargs:
            formatter = kwargs["formatter"]

        self.formatter = formatter

        if "console" in kwargs:
            self.console = kwargs["console"]

        if self.console is None:
            self.console = Console()

        if self.live is None:
            self.uri_table = Table()

            # TODO: Add columns based on config
            self.uri_table.add_column("Method")
            self.uri_table.add_column("URI")
            self.uri_table.add_column("Status")
            self.uri_table.add_column("Size")
            self.uri_table.add_column("Time")

            self.live = Live(self.uri_table, auto_refresh=False)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            request = Request(record)

            if request.is_valid:
                if not request.is_loggable:
                    return

                time = self.formatter.formatTime(record, datefmt=self.formatter.datefmt)

                self.uri_table.add_row(
                    Text(request.method, style=request.style),
                    Text(request.uri, style="white bold"),
                    Text(request.status, style=request.style),
                    Text(request.size),
                    Text(time),
                )
                self.live.start()
                self.live.refresh()

                self.flush()
            else:
                super().emit(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as ex:
            # self.handleError(record)
            print(ex)
