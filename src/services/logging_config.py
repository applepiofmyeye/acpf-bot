"""Logging configuration for ACPF Bot."""

import logging
import os
import sys

# Map log level strings to logging constants
LOG_LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured log messages."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured fields."""
        # Base log message
        parts = [
            f"[{record.levelname}]",
            f"{record.name}:{record.funcName}:{record.lineno}",
            record.getMessage(),
        ]

        # Add extra fields if present (check __dict__ instead of hasattr)
        record_dict = record.__dict__
        if "telegram_user_id" in record_dict:
            parts.append(f"user_id={record_dict['telegram_user_id']}")
        if "state" in record_dict:
            parts.append(f"state={record_dict['state']}")
        if "event" in record_dict:
            parts.append(f"event={record_dict['event']}")
        if "sheet_name" in record_dict:
            parts.append(f"sheet={record_dict['sheet_name']}")
        if "spreadsheet_id_suffix" in record_dict:
            parts.append(
                f"spreadsheet_id_suffix={record_dict['spreadsheet_id_suffix']}"
            )

        return " | ".join(parts)


def setup_logging() -> None:
    """Configure logging for the application."""
    # Get log level from environment (default to INFO)
    # Read directly from env to avoid circular import with config
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level_int = LOG_LEVEL_MAP.get(log_level_str, logging.INFO)

    # Create logger
    logger = logging.getLogger("acpf_bot")
    logger.setLevel(log_level_int)

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level_int)

    # Set formatter
    formatter = StructuredFormatter()
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"acpf_bot.{name}")


# Setup logging on module import
setup_logging()
