import enum
import logging
import typing

from django.core.management.color import color_style
from django.db.migrations import Migration

__all__ = ["Severity", "MigrationLogger", "SeverityLiteral"]

StyleCallable = typing.Callable[[typing.AnyStr], typing.AnyStr]
SeverityLiteral = typing.Literal[0, 1, 2, 3, 4]

_severityToLoglevel: typing.Dict[int, int] = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG,
}

_style = color_style()
_severityToStyle: typing.Dict[int, StyleCallable] = {
    0: _style.ERROR,
    1: _style.ERROR,
    2: _style.WARNING,
    3: _style.NOTICE,
    4: _style.NOTICE,
}


class Severity(enum.IntEnum):
    CRITICAL = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4

    @property
    def loglevel(self) -> int:
        return _severityToLoglevel[self.value]

    @property
    def style(self) -> StyleCallable:
        return _severityToStyle[self.value]


class MigrationLogger:
    def __init__(
        self,
        migration: Migration,
        stream: typing.Optional[typing.IO] = None,
        logger: typing.Optional[logging.Logger] = None,
    ):
        self.migration = migration
        self.stream = stream
        self.logger = logger

    def log(self, sev: Severity, msg: str):
        _msg = f"[{self.migration.app_label}.{self.migration.name}] {msg}"
        if self.logger:
            self.logger.log(sev.loglevel, _msg)
        if self.stream:
            _msg = sev.style(f"[{sev.name}] {_msg}\n")
            self.stream.write(_msg)
