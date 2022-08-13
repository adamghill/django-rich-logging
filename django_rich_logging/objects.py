import logging
import re
from dataclasses import dataclass

from django.conf import settings


REQUEST_REGEX = (
    r"(GET|POST|PATCH|UPDATE|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE)\s+([\S]+)\s+([\S]+)"
)


@dataclass
class Request:
    """
    Handles parsing the `LogRecord` into a `Request` object which has the correct data.
    """

    method: str
    uri: str
    status: str
    size: str
    style: str = None
    is_valid: bool = False

    def __init__(self, record: logging.LogRecord):
        # Ignore any message from `django.server` that doesn't have 3 args.
        # TODO: Find a less hacky way to deal with this.
        if record.name != "django.server" or len(record.args) != 3:
            return

        unparsed_request = record.args[0]

        # Example: GET /profile HTTP/1.1
        matches = re.match(REQUEST_REGEX, unparsed_request)

        if matches:
            self.is_valid = True

            self.method = matches.group(1)
            self.uri = matches.group(2)

            self.status = record.args[1]
            self.size = record.args[2]

            self.style = self.get_style()

    def get_style(self):
        if self.status.startswith("2"):
            return "green"
        elif self.status.startswith("3"):
            return "yellow"
        elif self.status.startswith("4"):
            return "yellow"
        elif self.status.startswith("5"):
            return "red"

    @property
    def is_loggable(self):
        if settings.STATIC_URL and self.uri.startswith(settings.STATIC_URL):
            return False

        if self.uri == "/favicon.ico":
            return False

        return True
