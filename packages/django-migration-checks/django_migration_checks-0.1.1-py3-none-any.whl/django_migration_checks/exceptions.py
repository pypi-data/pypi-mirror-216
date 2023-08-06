class DJMCError(Exception):
    pass


class MigrationCheckError(DJMCError):
    pass


class InvalidMigrationCheck(MigrationCheckError):
    pass


class DuplicateMigrationCheck(MigrationCheckError):
    pass


class TerminalRequired(DJMCError):
    pass
