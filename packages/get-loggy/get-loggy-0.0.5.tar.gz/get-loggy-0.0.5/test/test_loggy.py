import logging
from logging import Logger

import pytest

from conftest import CustomLogFormatter
from loggy import loggy
from loggy.exceptions import MutuallyExclusiveArgumentsError


def test_log_format():
    log_format = ("(%(filename)s:%(lineno)d:%(funcName)s)", "%m-%d-%Y %I:%M:%S %p %Z")
    log = loggy.get_loggy(log_format=log_format)
    log.info("test")
    assert log.handlers[0].formatter._fmt == log_format[0]


def test_log_initiates():
    log = loggy.get_loggy()
    assert type(log) == Logger


def test_mutually_exclusive_args():
    with pytest.raises(MutuallyExclusiveArgumentsError):
        loggy.get_loggy(
            use_color=True,
            log_file={"filename": "some-file.log"},
        )


def test_custom_log_level():
    loggy.addLoggingLevel("TRACE", logging.DEBUG - 5)
    loggy.get_loggy()
    assert hasattr(logging, "TRACE")


def test_log_file(tmp_path):
    tmp_file = tmp_path / "log_file.log"
    log = loggy.get_loggy(log_file={"filename": tmp_file})
    assert tmp_path.exists()

    log.info("Test")
    with tmp_file.open() as f:
        lines = f.readlines()
        assert len(lines) == 1


def test_custom_log_level_add_color():
    loggy.addLoggingLevel("CUSTOM_LEVEL", logging.DEBUG - 5)
    additional_color = {logging.CUSTOM_LEVEL: "\033[38;20m"}

    custom_formatter = CustomLogFormatter(
        color_dict=additional_color
    )

    log = loggy.get_loggy()
    log.handlers[0].formatter = custom_formatter

    handler_colors = log.handlers[0].formatter.COLORS

    assert logging.CUSTOM_LEVEL in handler_colors
    assert additional_color[logging.CUSTOM_LEVEL] == handler_colors[logging.CUSTOM_LEVEL]

