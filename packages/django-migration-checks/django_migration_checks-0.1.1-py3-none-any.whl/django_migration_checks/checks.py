import logging
import typing
from abc import ABC, abstractmethod

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations import Migration
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState

from django_migration_checks.logging import MigrationLogger, Severity, SeverityLiteral
from django_migration_checks.messages import (
    MigrationCheckMessage,
    MigrationCheckMessagePool,
)
from django_migration_checks.types import MigrationPlan

__all__ = [
    "PreMigrationCheck",
    "PostMigrationCheck",
    "MigrationCheckResult",
]

MigrationCheckResult = typing.NamedTuple(
    "MigrationCheckResult",
    [("exiting", bool), ("msg_count", int), ("filtered", bool)],
)


class BaseMigrationCheck(ABC):
    def __init__(
        self,
        migration: Migration,
        backwards: bool,
        schema_editor: BaseDatabaseSchemaEditor,
        project_state: ProjectState,
        plan: MigrationPlan,
        loader: MigrationLoader,
        stream: typing.Optional[typing.IO] = None,
        logger: typing.Optional[logging.Logger] = None,
    ):
        self.migration = migration
        self.backwards = backwards
        self.schema_editor = schema_editor
        self.project_state = project_state
        self.plan = plan
        self.loader = loader

        migration_logger = MigrationLogger(self.migration, stream, logger)
        self.messages = MigrationCheckMessagePool(migration_logger)

    def add_message(
        self,
        message: str,
        severity: typing.Union[Severity, SeverityLiteral] = Severity.INFO,
        prompting: bool = False,
        exiting: bool = False,
    ):
        if not isinstance(severity, Severity):
            severity = Severity(severity)
        self.messages.add(MigrationCheckMessage(message, severity, prompting, exiting))

    @abstractmethod
    def validate(self):
        raise NotImplementedError  # pragma: no cover

    def filter(self) -> bool:
        return False

    def evaluate(self, suppress_prompts: bool = False) -> MigrationCheckResult:
        if self.filter():
            return MigrationCheckResult(exiting=False, msg_count=0, filtered=True)
        self.validate()
        evaluated = self.messages.evaluate(True, suppress_prompts)
        exiting = False
        for i in evaluated:
            if i.exiting:
                exiting = True
                break
        return MigrationCheckResult(
            exiting=exiting,
            msg_count=len(evaluated),
            filtered=False,
        )


class PreMigrationCheck(BaseMigrationCheck, ABC):
    pass


class PostMigrationCheck(BaseMigrationCheck, ABC):
    pass
