"""
Module defining exceptions used in the package
"""


# For backwards compatibility
class MissingConfigurationFile(Exception):
    pass


class InvalidSchedule(Exception):
    pass


# / backwards compatibility
class NotFoundError(Exception):
    pass


class APIKeyMissingError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class APIDataExtractError(Exception):
    pass


class MissingConfigurationFileError(MissingConfigurationFile):
    pass


class NoDataError(Exception):
    pass


class NoComfortProfileError(NoDataError):
    pass


class InvalidScheduleError(InvalidSchedule):
    pass
