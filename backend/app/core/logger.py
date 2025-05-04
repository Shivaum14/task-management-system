"""Logger package."""

import copy
import logging
from typing import Any, MutableMapping, Tuple


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


class MergeLoggerAdapter(logging.LoggerAdapter):  # type: ignore
    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> Tuple[Any, MutableMapping[str, Any]]:
        """
        Process the Logging message and keyword arguments passed in to
        a logging call to insert contextual information. The extra argument
        of the LoggerAdapter will be merged with the extra argument of the
        logging call where the logging call's argument take precedence.
        """
        try:
            kwargs["extra"] = {**self.extra, **kwargs["extra"]}  # type: ignore
        except KeyError:  # pragma: no cover
            kwargs["extra"] = self.extra  # pragma: no cover
        return msg, kwargs
