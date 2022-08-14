import logging
from string import Template
from typing import Dict

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

from .objects import RequestRecord


DEFAULT_COLUMNS = [
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
]


class DjangoRequestHandler(logging.StreamHandler):
    """
    A logging handler that prints Django requests in a live-updating table.
    """

    live = None
    table = None
    console = None
    columns = None

    def __init__(self, *args, **kwargs):
        super().__init__()

        if "columns" in kwargs:
            self.columns = kwargs["columns"]
        else:
            self.columns = DEFAULT_COLUMNS

        if "console" in kwargs:
            self.console = kwargs["console"]

        if self.console is None:
            self.console = Console()

        if self.live is None:
            self.table = Table()
            self._add_column_headers()

            self.live = Live(self.table, auto_refresh=False)

    def _add_column_headers(self):
        """
        Add column headers for each column.
        """

        for column in self.columns:
            self.table.add_column(column["header"])

    def _add_row(self, request_record: RequestRecord) -> None:
        """
        Add a row to the live updating table that includes rendered markup for each column.
        """

        row_columns = []

        for column in self.columns:
            markup = self._get_markup(request_record, column)
            text = Text.from_markup(markup, style=request_record.text_style)

            row_columns.append(text)

        self.table.add_row(*row_columns)

    def _get_markup(self, request_record: RequestRecord, column: Dict) -> str:
        """
        Get markup based on the column's `format` and the `RequestRecord` object.
        """

        format = column.get("format", "")
        style = column.get("style", "%")
        date_format = column.get("datefmt")

        if style == "%":
            return format % request_record.get_dict(date_format=date_format)
        elif style == "{":
            return format.format(**request_record.get_dict(date_format=date_format))
        elif style == "$":
            template = Template(format)

            return template.substitute(
                **request_record.get_dict(date_format=date_format)
            )
        else:
            raise Exception(f"Unknown style: {style}")

    def emit(self, record: logging.LogRecord) -> None:
        """
        Writes the logging record. If it's a request, add the record to a live,
        updating table. If not, emit it like normal.
        """

        try:
            request_record = RequestRecord(record)

            if request_record.is_valid:
                if not request_record.is_loggable:
                    return

                self._add_row(request_record)

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
