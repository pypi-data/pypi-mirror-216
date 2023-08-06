import sys
import typing
from dataclasses import dataclass

from django_migration_checks.exceptions import TerminalRequired
from django_migration_checks.logging import MigrationLogger, Severity

__all__ = ["MigrationCheckMessage", "MigrationCheckMessagePool"]


@dataclass
class MigrationCheckMessage:
    message: str
    severity: Severity
    prompting: bool
    exiting: bool

    def __hash__(self):
        return hash("".join([str(i) for i in (self.message, self.severity)]))

    def confirm(self):
        if not self.prompting:
            return
        if not sys.stdout.isatty():
            raise TerminalRequired
        resp = input("Continue? [y/N]: ")
        if resp.lower().strip() != "y":
            self.exiting = True

    def evaluate(self, logger: MigrationLogger) -> "MigrationCheckMessage":
        logger.log(self.severity, self.message)
        if self.prompting:
            self.confirm()
        return self


class MigrationCheckMessagePool:
    def __init__(self, logger: MigrationLogger):
        self.logger = logger
        self._items: typing.Set[MigrationCheckMessage] = set()

    @property
    def items(self) -> typing.FrozenSet[MigrationCheckMessage]:
        return frozenset(self._items)

    def add(self, message: MigrationCheckMessage):
        self._items.add(message)

    def clear(self):
        self._items.clear()

    def evaluate(
        self, evict: bool = False, suppress_prompts: bool = False
    ) -> typing.List[MigrationCheckMessage]:
        evaluated = []
        for item in self.items:
            if suppress_prompts and item.prompting:
                item.prompting = False
            evaluated.append(item.evaluate(self.logger))
            if evict:
                self._items.remove(item)
        return evaluated
