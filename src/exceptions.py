from builtins import super


class StratumBaseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class VersionError(StratumBaseException):
    def __init__(self, message):
        super(VersionError, self).__init__(message)


class SettingsError(StratumBaseException):
    def __init__(self, message):
        super(SettingsError, self).__init__(message)
