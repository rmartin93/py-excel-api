"""
Logging configuration for the Excel API application.

Python's logging system is more structured than console.log in Node.js.
It provides levels, formatters, handlers, and automatic file rotation.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from app.core.config import settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to console output.
    
    Similar to using chalk or colors in Node.js, but built into the logger.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Get the original formatted message
        message = super().format(record)
        
        # Add color based on log level
        color = self.COLORS.get(record.levelname, '')
        if color and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            return f"{color}{message}{self.RESET}"
        return message


def setup_logging() -> logging.Logger:
    """Configure application logging with both console and file output.
    
    This creates a logger that:
    - Outputs colored logs to console (like console.log but better)
    - Writes structured logs to rotating files
    - Handles different log levels (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    
    # Create main application logger
    logger = logging.getLogger("excel_api")
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Clear any existing handlers (prevents duplicate logs)
    logger.handlers.clear()
    
    # Console Handler (like console.log but with levels and colors)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Console format - clean and readable for development
    console_format = ColoredFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File Handler with rotation (like winston in Node.js)
    if settings.log_file_rotation:
        # Ensure logs directory exists
        log_dir = Path(settings.logs_dir)
        log_dir.mkdir(exist_ok=True)
        
        # Rotating file handler - creates new files when size limit reached
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / "application.log",
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # File format - more detailed for debugging
        file_format = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # Separate error log file
        error_handler = logging.handlers.RotatingFileHandler(
            filename=log_dir / "error.log",
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_format)
        logger.addHandler(error_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
        
    Returns:
        Logger instance
        
    Usage:
        # In any module
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("This is an info message")
    """
    if name is None:
        name = "excel_api"
    
    return logging.getLogger(name)


# Initialize logging when this module is imported
# This ensures logging is set up before any other code runs
_logger = setup_logging()


# Example usage functions for different log levels
def log_request(method: str, path: str, status_code: int, duration_ms: float):
    """Log HTTP request information.
    
    Example of structured logging for API requests.
    Similar to morgan middleware in Express.
    """
    logger = get_logger("excel_api.requests")
    logger.info(
        f"{method} {path} - {status_code} - {duration_ms:.2f}ms"
    )


def log_excel_generation(template_name: str, success: bool, duration_ms: float):
    """Log Excel generation events.
    
    Example of business logic logging.
    """
    logger = get_logger("excel_api.excel")
    if success:
        logger.info(f"Excel generated successfully: {template_name} ({duration_ms:.2f}ms)")
    else:
        logger.error(f"Excel generation failed: {template_name}")


def log_error(error: Exception, context: Optional[str] = None):
    """Log errors with full traceback.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error happened
    """
    logger = get_logger("excel_api.errors")
    message = f"Error: {str(error)}"
    if context:
        message = f"{context} - {message}"
    
    # Log with full traceback for debugging
    logger.error(message, exc_info=True)
