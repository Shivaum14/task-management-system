"""Logger package."""

import copy
import logging
from typing import Any


class ConsoleFormatter(logging.Formatter):
    """Custom log formatter adding 'extra' fields to the nicelog module."""

    ignore_keys = {
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "color_message",
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        from nicelog.formatters import Colorful  # type: ignore
        from nicelog.styles.base import BaseStyle  # type: ignore

        style = BaseStyle()
        style.logger_name = dict(fg="black", bg="grey")
        self.fmt = Colorful(show_date=True, show_function=False, show_filename=True, message_inline=True, style=style)

    def format(self, record: logging.LogRecord) -> str:
        record = copy.copy(record)  # Needed to prevent mutation of record.msg.
        kv = " ".join([f"{k}={record.__dict__[k]}" for k in set(record.__dict__.keys()).difference(self.ignore_keys)])
        record.msg = f"{record.msg} {kv}"
        return self.fmt.format(record)
