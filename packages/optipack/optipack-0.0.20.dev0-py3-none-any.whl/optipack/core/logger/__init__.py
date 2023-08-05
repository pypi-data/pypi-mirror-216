from optipack.core.logger.otp_logger import *

LOGGER_MAPPER = dict(
    console=BaseLogger,
    file=FileLogger,
    splunk=SplunkLogger
)
