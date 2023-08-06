import logging
import sys
import typing

from django.conf import settings

__all__ = [
    "MIGRATION_CHECKS_CLASSES",
    "MIGRATION_CHECKS_ENABLED",
    "MIGRATION_CHECKS_LOGGER",
    "MIGRATION_CHECKS_STREAM",
]

MIGRATION_CHECKS_CLASSES: typing.List[str] = getattr(
    settings,
    "MIGRATION_CHECKS_CLASSES",
    [],
)
MIGRATION_CHECKS_ENABLED: bool = getattr(
    settings,
    "MIGRATION_CHECKS_ENABLED",
    True,
)
MIGRATION_CHECKS_LOGGER: typing.Optional[typing.Union[logging.Logger, str]] = getattr(
    settings,
    "MIGRATION_CHECKS_LOGGER",
    None,
)
MIGRATION_CHECKS_STREAM: typing.Optional[typing.IO] = getattr(
    settings,
    "MIGRATION_CHECKS_STREAM",
    sys.stdout,
)
