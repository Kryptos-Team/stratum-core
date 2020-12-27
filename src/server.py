from .log import Logger

log = Logger(name=__name__, tag="stratum.server")
log.debug("Test")
