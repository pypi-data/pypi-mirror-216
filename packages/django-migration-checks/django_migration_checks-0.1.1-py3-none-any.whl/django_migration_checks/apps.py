import importlib
import typing

from django.apps import AppConfig
from django.core.signals import setting_changed
from django.db.models.signals import post_migrate, pre_migrate
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

if typing.TYPE_CHECKING:
    from django_migration_checks.handler import (
        MigrationCheckHandler,  # pragma: no cover
    )


class DJMigrationChecks(AppConfig):
    name = "django_migration_checks"
    verbose_name = _("Django Migration Checks")
    settings_prefix = "MIGRATION_CHECKS_"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = None
        self.settings = None

    def init_logging(self):
        self.handler.logger = self.settings.MIGRATION_CHECKS_LOGGER
        self.handler.stream = self.settings.MIGRATION_CHECKS_STREAM

    def toggle_checks(self):
        if self.settings.MIGRATION_CHECKS_ENABLED:
            pre_migrate.connect(self.handler.pre_evaluate)
            post_migrate.connect(self.handler.post_evaluate)
        else:
            pre_migrate.disconnect(self.handler.pre_evaluate)
            post_migrate.disconnect(self.handler.post_evaluate)

    def register_checks(self):
        self.handler.clear_checks()
        for check_path in self.settings.MIGRATION_CHECKS_CLASSES:
            self.handler.register_check(import_string(check_path), check_path)

    def reload_settings(self, **kwargs):
        setting = kwargs["setting"]
        if not setting.startswith(self.settings_prefix):
            return
        importlib.reload(self.settings)
        if setting == "MIGRATION_CHECKS_CLASSES":
            self.register_checks()
        elif setting == "MIGRATION_CHECKS_ENABLED":
            self.toggle_checks()
        elif setting in {"MIGRATION_CHECKS_STREAM", "MIGRATION_CHECKS_LOGGER"}:
            self.init_logging()

    def ready(self):
        from django_migration_checks import settings as app_settings
        from django_migration_checks.handler import MigrationCheckHandler

        self.settings = app_settings
        self.handler = MigrationCheckHandler()
        self.init_logging()
        self.register_checks()
        self.toggle_checks()
        setting_changed.connect(self.reload_settings)
