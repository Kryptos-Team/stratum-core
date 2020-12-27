import logging
from colorama import Fore, Style
from fluent import handler
from src import settings
from .symbols import Symbol
from .utils import is_supported


class LogFormatter(logging.Formatter):
    _fmt = settings.log["format"]

    if is_supported():
        error_fmt = _fmt.format(color=Fore.RED, colwidth=10, end=Style.RESET_ALL, symbol=Symbol.ERROR.value)
        info_fmt = _fmt.format(color=Fore.BLUE, colwidth=10, end=Style.RESET_ALL, symbol=Symbol.INFO.value)
        warning_fmt = _fmt.format(color=Fore.YELLOW, colwidth=10, end=Style.RESET_ALL, symbol=Symbol.WARNING.value)
        debug_fmt = _fmt.format(color=Fore.LIGHTBLACK_EX, colwidth=10, end=Style.RESET_ALL, symbol=Symbol.INFO.value)
        success_fmt = _fmt.format(color=Fore.LIGHTGREEN_EX, colwidth=10, end=Style.RESET_ALL,
                                  symbol=Symbol.SUCCESS.value)
        critical_fmt = _fmt.format(color=Fore.LIGHTRED_EX, colwidth=10, end=Style.RESET_ALL, symbol=Symbol.ERROR.value)
    else:
        _fmt = _fmt.replace("{color}", "").replace("{end}", "").strip(" ")

        error_fmt = _fmt.format(symbol=Symbol.ERROR.value)
        info_fmt = _fmt.format(symbol=Symbol.INFO.value)
        warning_fmt = _fmt.format(symbol=Symbol.WARNING.value)
        debug_fmt = _fmt.format(symbol=Symbol.INFO.value)
        success_fmt = _fmt.format(symbol=Symbol.SUCCESS.value)
        critical_fmt = _fmt.format(symbol=Symbol.ERROR.value)

    def __init__(self):
        super(LogFormatter, self).__init__(fmt=settings.log["format"], datefmt=None)

    def format(self, record: logging.LogRecord) -> str:
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        try:
            format = self._style._fmt
        except AttributeError:
            format = self._fmt

        # Replace the original format
        if record.levelno == logging.DEBUG:
            if hasattr(self, "_style"):
                self._style._fmt = LogFormatter.debug_fmt
            self._fmt = LogFormatter.debug_fmt
        elif record.levelno == logging.INFO:
            if hasattr(self, "_style"):
                self._style._fmt = LogFormatter.info_fmt
            self._fmt = LogFormatter.info_fmt
        elif record.levelno == logging.WARNING:
            if hasattr(self, "_style"):
                self._style._fmt = LogFormatter.warning_fmt
            self._fmt = LogFormatter.warning_fmt
        elif record.levelno == logging.ERROR:
            if hasattr(self, "_style"):
                self._style._fmt = LogFormatter.error_fmt
            self._fmt = LogFormatter.error_fmt
        elif record.levelno == logging.CRITICAL:
            if hasattr(self, "_style"):
                self._style._fmt = LogFormatter.critical_fmt
            self._fmt = LogFormatter.critical_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original formatter
        if hasattr(self, "_style"):
            self._style._fmt = format
        self._fmt = format

        return result


class FluentdFormatter(handler.FluentRecordFormatter):
    def __init__(self):
        structure = {
            "hostname": "%(hostname)s",
            "module": "%(module)s",
            "funcName": "%(funcName)s",
            "levelname": "%(levelname)s",
            "created": "%(created)f",
            "process": "%(process)d",
            "thread": "%(thread)d",
            "processName": "%(processName)s",
            "pathName": "%(pathname)s",
            "levelno": "%(levelno)s",
            "stack_trace": "%(exc_text)s",
            "message": "%(message)s"
        }
        super(FluentdFormatter, self).__init__(structure)
