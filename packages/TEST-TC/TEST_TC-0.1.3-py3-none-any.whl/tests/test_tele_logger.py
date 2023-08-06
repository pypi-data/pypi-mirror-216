import os
import logging
from logging import DEBUG
from time import localtime, strftime
from utility.tele_logger import Logger

def test_logger_initialization():
    logger = Logger()
    assert isinstance(logger.logger, logging.Logger)
    assert isinstance(logger.important_logger, logging.Logger)
    assert logger.name is None

def test_logger_initialize_logger(tmpdir):
    logger = Logger()
    logger.initialize_logger("test_session")

    # Check if log files are created
    log_folder = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], "logs")
    assert os.path.exists(log_folder)

    log_files = os.listdir(log_folder)
    assert f"test_session_{strftime('%Y%m%d', localtime())}.log" in log_files
    assert f"test_session_verbose_{strftime('%Y%m%d', localtime())}.log" in log_files

def test_logger_info_important(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    logger.info("This is an info message", important = True)

    assert len(caplog.records) == 2
    assert caplog.records[0].message == "This is an info message"
    assert caplog.records[1].message == "This is an info message"

def test_logger_info(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    logger.info("This is an info message")

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "This is an info message"

def test_logger_error(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    logger.error("This is an error message")

    assert len(caplog.records) == 2
    assert caplog.records[0].message == "This is an error message"
    assert caplog.records[1].message == "This is an error message"

def test_logger_exception(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    try:
        1 / 0
    except ZeroDivisionError as e:
        logger.exception("An exception occurred")

    assert len(caplog.records) == 2
    assert caplog.records[0].message == "An exception occurred"
    assert caplog.records[1].message == "An exception occurred"

def test_logger_warning(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    logger.warning("This is a warning message")

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "This is a warning message"

def test_logger_debug_not_init(caplog):
    logger = Logger()
    logger.initialize_logger("test_session")

    logger.debug("This is a debug message")

    assert len(caplog.records) == 0

def test_logger_debug_init(caplog):
    logger = Logger(level=DEBUG)
    logger.initialize_logger("test_session")

    logger.debug("This is a debug message")

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "This is a debug message"
