from enum import Enum
from colorama import init, deinit, Fore
from .utils import is_supported

init(autoreset=True)

_MAIN = {
    "info": "ℹ",
    "success": "✔",
    "warning": "⚠",
    "error": "✖"
}

_FALLBACKS = {
    "info": "i",
    "success": "v",
    "warning": "!!",
    "error": "x"
}

symbols = _MAIN if is_supported() else _FALLBACKS


class Symbol(Enum):
    if is_supported():
        INFO = Fore.BLUE + symbols["info"] + Fore.RESET
        SUCCESS = Fore.GREEN + symbols["success"] + Fore.RESET
        WARNING = Fore.YELLOW + symbols["warning"] + Fore.RESET
        ERROR = Fore.RED + symbols["error"] + Fore.RESET
    else:
        INFO = symbols["info"]
        SUCCESS = symbols["success"]
        WARNING = symbols["warning"]
        ERROR = symbols["error"]


deinit()
