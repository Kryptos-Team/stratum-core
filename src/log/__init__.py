import logging
import src.settings as settings
from .handler import FluentdHandler, LogHandler


class Logger(logging.Logger):
    def __init__(self, name, tag=None):
        # Make sure name is not None
        if name is None:
            name = __name__
        # Initialize logger
        logger = logging.getLogger(name)

        # Setup stream/fluentd handler
        if settings.log["fluentd"]["enabled"]:
            # Initialize fluentd formatter
            stderr = FluentdHandler(tag)
            stdout = FluentdHandler(tag)
        else:
            stderr = LogHandler()
            stdout = LogHandler()
        logger.addHandler(stdout)
        logger.addHandler(stderr)
        logger.setLevel(settings.log["level"])

        logger.debug(f"Logger initialized with fluentd: {settings.log['fluentd']['enabled']}")
        logger.debug(f"Logging level set to {settings.log['level']}")

        super(Logger, self).__init__(name, settings.log["level"])
