import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ShortNameFormatter(logging.Formatter):
    """A logging formatter that shortens the logger name.

    Formats the logger name by taking only the last component
    of the full logger path.
    """

    def format(self, record):
        """Format the log record with a shortened logger name.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        record.name = record.name.split(".")[-1]
        return super().format(record)


def setup_logger(name: str = "app") -> logging.Logger:
    """Configure and return the application logger.

    Sets up a logger named `name` with a console handler that uses
    ShortNameFormatter at DEBUG level.

    Args:
        name (str): The name of the logger. Default is "app".

    Returns:
        logging.Logger: The configured logger instance.
    """
    base_logger = logging.getLogger(name=name)
    base_logger.setLevel(logging.DEBUG)

    formatter = ShortNameFormatter(
        "[%(asctime)s][%(name)12s][%(levelname)8s]: %(message)s"
    )

    ch = logging.StreamHandler()
    ch.name = "console"
    # level = logging.DEBUG if "-q" not in sys.argv else logging.INFO
    level = logging.DEBUG
    ch.setLevel(level)
    ch.setFormatter(formatter)
    base_logger.addHandler(ch)

    return base_logger


default_logger = setup_logger()
