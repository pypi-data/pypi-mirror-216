import logging
import sys
import threading
import typing
from collections import deque

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations import Migration
from django.db.migrations.loader import MigrationLoader

from django_migration_checks.checks import PostMigrationCheck, PreMigrationCheck
from django_migration_checks.exceptions import (
    DuplicateMigrationCheck,
    InvalidMigrationCheck,
)
from django_migration_checks.logging import MigrationLogger
from django_migration_checks.types import ReceiverKwargs

MigrationCheck = typing.Union[
    typing.Type[PreMigrationCheck],
    typing.Type[PostMigrationCheck],
]
CheckPool = typing.Dict[str, MigrationCheck]

__all__ = ["MigrationCheckHandler"]


class MigrationCheckHandler:
    def __init__(
        self,
        logger: typing.Optional[typing.Union[str, logging.Logger]] = None,
        stream: typing.Optional[typing.IO] = None,
    ):
        self.logger = logger  # type: ignore
        self.stream = stream

        self._lock = threading.Lock()
        self._signal_buffer: typing.Deque[int] = deque([], maxlen=16)
        self._pre_checks: CheckPool = {}
        self._post_checks: CheckPool = {}

    @property
    def logger(self) -> typing.Optional[logging.Logger]:
        return getattr(self, "_logger", None)

    @logger.setter
    def logger(self, value: typing.Optional[typing.Union[str, logging.Logger]]):
        if isinstance(value, str):
            value = logging.getLogger(value)
        self._logger = value

    def get_migration_logger(self, migration: Migration) -> MigrationLogger:
        return MigrationLogger(migration, self.stream, self.logger)

    @property
    def pre_checks(self) -> CheckPool:
        return self._pre_checks.copy()

    @property
    def post_checks(self) -> CheckPool:
        return self._post_checks.copy()

    @staticmethod
    def get_connection(using: str) -> BaseDatabaseWrapper:
        return connections[using]

    def get_loader(self, using: str) -> MigrationLoader:
        return MigrationLoader(self.get_connection(using), replace_migrations=False)

    def register_check(self, cls: MigrationCheck, name: str):
        if issubclass(cls, PreMigrationCheck):
            check_pool = self._pre_checks
        elif issubclass(cls, PostMigrationCheck):
            check_pool = self._post_checks
        else:
            raise InvalidMigrationCheck

        if name in check_pool:
            raise DuplicateMigrationCheck
        check_pool[name] = cls

    def deregister_check(self, name: str):
        self._pre_checks.pop(name, None)
        self._post_checks.pop(name, None)

    def clear_checks(self):
        self._pre_checks = {}
        self._post_checks = {}

    def terminate(self):
        try:
            self._lock.release()
        except RuntimeError:
            pass
        sys.exit(1)

    def _evaluate(self, pool: CheckPool, **kwargs):
        kwargs = typing.cast(ReceiverKwargs, kwargs)  # type: ignore
        with self._lock:  # Only respond to a given signal once
            _hash = hash(kwargs["signal"])
            if _hash in self._signal_buffer:
                return  # pragma: no cover
            self._signal_buffer.appendleft(_hash)

        loader = self.get_loader(kwargs["using"])
        state = None
        exiting = False
        for migration, backwards in (plan := kwargs["plan"]):
            if state is None:
                state = loader.project_state(
                    (migration.app_label, migration.name),
                    at_end=False,
                )
            with loader.connection.schema_editor(  # type: ignore
                collect_sql=True,
                atomic=migration.atomic,
            ) as schema_editor:
                if not backwards:
                    state = migration.apply(state, schema_editor, collect_sql=True)
                else:
                    state = migration.unapply(state, schema_editor, collect_sql=True)
                for check_cls in pool.values():
                    check_obj = check_cls(
                        migration,
                        backwards,
                        schema_editor,
                        state,  # type: ignore
                        plan,
                        loader,
                        self.stream,
                        self.logger,
                    )
                    result = check_obj.evaluate(exiting)
                    if not exiting and result.exiting:
                        exiting = True
        if exiting:
            self.terminate()

    def pre_evaluate(self, **kwargs):
        self._evaluate(self.pre_checks, **kwargs)

    def post_evaluate(self, **kwargs):
        self._evaluate(self.post_checks, **kwargs)
