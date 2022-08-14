import logging
import re
from dataclasses import dataclass
from datetime import datetime

from django.conf import settings


REQUEST_REGEX = (
    r"(GET|POST|PATCH|UPDATE|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE)\s+([\S]+)\s+([\S]+)"
)


@dataclass
class RequestRecord:
    """
    Handles parsing the `logging.LogRecord` into a `RequestRecord` object.
    """

    method: str
    path: str
    status_code: str
    size: str
    created: datetime
    record: logging.LogRecord
    text_style: str = None
    is_valid: bool = False

    def __init__(self, record: logging.LogRecord):
        # Ignore any message from `django.server` that doesn't have 3 args.
        # TODO: Find a less hacky way to deal with this.
        if record.name != "django.server" or len(record.args) != 3:
            return

        self.record = record
        self.created = datetime.fromtimestamp(record.created)

        unparsed_request = record.args[0]

        # Example: GET /profile HTTP/1.1
        matches = re.match(REQUEST_REGEX, unparsed_request)

        if matches:
            self.is_valid = True

            self.method = matches.group(1)
            self.path = matches.group(2)

            self.status_code = record.args[1]
            self.size = record.args[2]

            self.text_style = self.get_text_style()

    def get_text_style(self):
        if self.status_code.startswith("2"):
            return "green"
        elif self.status_code.startswith("3"):
            return "yellow"
        elif self.status_code.startswith("4"):
            return "yellow"
        elif self.status_code.startswith("5"):
            return "red"

    @property
    def is_loggable(self):
        if settings.STATIC_URL and self.path.startswith(settings.STATIC_URL):
            return False

        if self.path == "/favicon.ico":
            return False

        return True

    def get_dict(self, date_format: str = None):
        created_str = str(self.created)

        if date_format:
            created_str = self.created.strftime(date_format)

        return {
            "created": created_str,
            "method": self.method,
            "path": self.path,
            "status_code": self.status_code,
            "size": self.size,
        }
