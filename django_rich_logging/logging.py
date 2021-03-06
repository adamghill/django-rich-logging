import logging
import re

from django.conf import settings

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text


class DjangoRequestHandler(logging.StreamHandler):
    """
    A logging handler that prints Django requests in a live-updating table.
    """

    live = None
    uri_table = None
    console = None

    def __init__(self, *args, **kwargs):
        super().__init__()

        if "console" in kwargs:
            self.console = kwargs["console"]

        if self.console is None:
            self.console = Console()

        if self.live is None:
            self.uri_table = Table()
            self.uri_table.add_column("Method")
            self.uri_table.add_column("URI")
            self.uri_table.add_column("Status")
            self.uri_table.add_column("Size")

            self.live = Live(self.uri_table, auto_refresh=False)

    def emit(self, record: logging.LogRecord) -> None:
        # Ignore any message from `django.server` that don't have 3 args.
        # There might be a better approach to this, not sure.
        if record.name != "django.server" or len(record.args) != 3:
            super().emit(record)
            return

        try:
            request = record.args[0]
            status = record.args[1]
            size = ""

            # Example: GET /profile HTTP/1.1
            matches = re.match(
                r"(GET|POST|PATCH|UPDATE|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE)\s+([\S]+)\s+([\S]+)",
                request,
            )

            if matches:
                method = matches.group(1)
                uri = matches.group(2)

                if (
                    not settings.STATIC_URL or not uri.startswith(settings.STATIC_URL)
                ) and not uri == "/favicon.ico":
                    style = None

                    if status.startswith("2"):
                        size = record.args[2]
                        style = "green"
                    elif status.startswith("3"):
                        style = "yellow"
                    elif status.startswith("4"):
                        style = "yellow"
                    elif status.startswith("5"):
                        style = "red"

                    self.uri_table.add_row(
                        Text(method, style=style),
                        Text(uri, style="white bold"),
                        Text(status, style=style),
                        Text(size),
                    )
                    self.live.start()
                    self.live.refresh()

            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as ex:
            # self.handleError(record)
            print(ex)
