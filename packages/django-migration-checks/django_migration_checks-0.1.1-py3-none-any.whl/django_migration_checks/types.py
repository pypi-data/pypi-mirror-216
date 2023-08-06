import typing

from django.apps import AppConfig
from django.db.migrations import Migration
from django.db.migrations.state import StateApps
from django.dispatch.dispatcher import Signal

__all__ = ["MigrationPlan", "ReceiverKwargs"]

MigrationPlan = typing.List[typing.Tuple[Migration, bool]]


class ReceiverKwargs(typing.TypedDict):
    signal: Signal
    sender: AppConfig
    app_config: AppConfig
    verbosity: int
    interactive: bool
    using: str
    apps: StateApps
    plan: MigrationPlan
