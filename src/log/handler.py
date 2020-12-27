from io import BytesIO
import msgpack
from fluent import handler
from .formatter import FluentdFormatter, LogFormatter
import src.settings as settings
import logging


class LogHandler(logging.StreamHandler):
    def __init__(self):
        super(LogHandler, self).__init__()
        self.setFormatter(LogFormatter())


class FluentdHandler(handler.FluentHandler):
    def __init__(self, tag):
        # Setup fluentd variables
        host = settings.log["fluentd"]["host"]
        port = settings.log["fluentd"]["port"]

        super(FluentdHandler, self).__init__(tag=tag, host=host, port=port,
                                             buffer_overflow_handler=self.overflow_handler)
        formatter = FluentdFormatter()
        self.setFormatter(formatter)

    def overflow_handler(self, pendings):
        unpacker = msgpack.Unpacker(BytesIO(pendings))
        for unpacked in unpacker:
            print(unpacked)
