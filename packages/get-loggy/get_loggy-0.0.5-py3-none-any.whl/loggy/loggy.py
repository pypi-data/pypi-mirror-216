import logging
from typing import Dict, Tuple

from .exceptions import exclusive_args

LOG_FORMAT = ("%(asctime)s | %(levelname)s | %(message)s | (%(filename)s:%(lineno)d:%(funcName)s) |", "%m-%d-%Y %I:%M:%S %p %Z")


class LogFormatter(logging.Formatter):
    """Formats custom log calls."""

    grey = "\033[38;20m"
    yellow = "\033[33;20m"
    red = "\033[31;20m"
    bold_red = "\033[31;1m"
    reset = "\033[0m"

    COLORS = {
        logging.DEBUG: grey,
        logging.INFO: grey,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }

    def __init__(self, *args, use_color: bool = False, **kwargs) -> None:
        """Initializes a `Formatter` with additional features.

        To use color we append colors to the original format at
        the front and back (color + fmt + reset). To avoid having the
        format polluted we keep a separate copy.
        """
        super().__init__(*args, **kwargs)
        self.use_color = use_color

        # set the original format so it can be overwritten
        # between operations
        self.original_fmt = self._fmt

    def format(self, record: logging.LogRecord) -> str:
        """Formats new records, optionally with color.

        Params:
            record (logging.LogRecord): Log to format.

        Returns:
            log_str (str): Formatted string representation of the log record.
        """

        color_fmt = None
        if self.use_color and self.original_fmt:
            log_fmt = self.COLORS.get(record.levelno, "")

            # Create a format to use for the colored output
            # using the original format from instantiation
            # to have a clean `self._fmt` between calls.
            color_fmt = log_fmt + self.original_fmt + self.reset

        log_str = logging.Formatter(color_fmt if color_fmt else self._fmt, self.datefmt).format(record)
        return log_str


def addLoggingLevel(level_name: str, level_number: int, method_name: str = None) -> None:
    """Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example:
        ```
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5
        ```

    Source:
        https://stackoverflow.com/a/35804945/12387496

    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(level_number):
            self._log(level_number, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(level_number, message, *args, **kwargs)

    logging.addLevelName(level_number, level_name)
    setattr(logging, level_name, level_number)
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


@exclusive_args(["use_color", "log_file"])
def get_loggy(log_level: str = "info",
              use_color: bool = False,
              log_format: Tuple[str, str] = None,
              log_file: Dict = None) -> logging.Logger:
    """Returns an instance of our custom `logging`.

    Logging should be used in place of printing, this
    ensures we get more information from the lines and it
    keeps us more organized by providing timestamps.

    Log format:
        `mm-dd-yyyy hh:mm:ss am/pm timezone | log level | message(s) | (filename:lineno:funcName)`

    Usage:
        ```python
        from loggy.loggy import get_loggy

        # always top level of the module
        log = get_loggy()

        # somewhere else in the code
        def do_something():
            log.info(f"something: {some_var_to_fstring_in}")

            try:
                # something
            catch Exception as e:
                log.exception(f"We caught an error: {e}")
        ```

    Params:
        log_level (str): Log level to utilize, this defaults to `info`,
            which won't print `debug` level. If you want `debug` then pass
            `get_loggy(log_level="debug")`.
        use_color (bool): Whether or not to have colored output. Defaults to
            `False`.
        log_format (Tuple[str, str]): Log format to overwrite the default.
            Example: `('%(asctime)s | %(levelname)s | %(message)s)', 'mm-dd-yyyy HH:MM:S'`
        log_file (Dict[str, str]): File path to a log file to create, including
            access type, encoding, delay, errors. See `logging.FileHandler` for kwargs.
            Example: `{"filename": "sample.log", "mode": "a"}`

    Returns:
        logger (Logger): A log class with access to `critical`, `debug`, `error`,
            `info`, and `warning` level logging.
    """
    logger = logging.getLogger(__package__)

    # Remove any existing handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.setLevel(log_level.upper())

    # Use an append-only file handler if filename supplied
    if log_file:
        handler = logging.FileHandler(**log_file if log_file else dict())
        handler.setFormatter(LogFormatter(*log_format if log_format else LOG_FORMAT))

    # Use stream if no filename supplied
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(
            LogFormatter(
                *log_format if log_format else LOG_FORMAT,
                use_color=use_color
            )
        )

    logger.addHandler(handler)

    return logger

