import os
import logging
import logging.handlers
import threading
from contextvars import ContextVar

# Define context variables for traceId and spanId
trace_id_var = ContextVar("trace_id", default=None)
span_id_var = ContextVar("span_id", default=None)


class CustomFormatter(logging.Formatter):
    LEVEL_COLORS = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]
    FORMATS = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {color}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m (traceId=%(traceId)s, spanId=%(spanId)s) -> %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, color in LEVEL_COLORS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        # Adding context data to record
        record.traceId = trace_id_var.get()
        record.spanId = span_id_var.get()

        output = formatter.format(record)
        # Remove the cache layer
        record.exc_text = None
        return output


# Define a lock for logger switching
logger_lock = threading.Lock()

def setup_logger(module_name: str) -> logging.Logger:
    with logger_lock:
        # create logger
        library, _, _ = module_name.partition(".py")
        logger = logging.getLogger(library)

        log_level = os.getenv("LOG_LEVEL", "INFO")
        level = logging.getLevelName(log_level.upper())
        logger.setLevel(level)

        # create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(CustomFormatter())
        # Add console handler to logger
        logger.addHandler(console_handler)

        if os.getenv("LOGGING") == "True":  # Check if logging is enabled
            # specify that the log file path is the same as `main.py` file path
            grandparent_dir = os.path.abspath(f"{__file__}/../../")
            log_name = os.getenv("LOG_FILE_NAME", "logger.log")
            log_path = os.path.join(grandparent_dir, log_name)
            # create local log handler
            try:
                log_handler = logging.handlers.RotatingFileHandler(
                    filename=log_path,
                    encoding="utf-8",
                    maxBytes=int(
                        os.getenv("LOG_MAX_BYTES", 32 * 1024 * 1024)
                    ),  # 32 MiB
                    backupCount=int(
                        os.getenv("LOG_BACKUP_COUNT", 2)
                    ),  # Rotate through 2 files
                )
                log_handler.setFormatter(CustomFormatter())
                log_handler.setLevel(level)
                logger.addHandler(log_handler)
            except Exception as e:
                logger.error(f"Failed to create file handler: {e}")

        return logger
