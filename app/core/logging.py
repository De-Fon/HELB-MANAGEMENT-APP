"""
Loguru logging configuration for the HELB backend.

Sets up:
  - Daily rotating log files (logs/app-YYYY-MM-DD.log)
  - Separate error log (logs/errors.log) with 7-day retention
  - Colored console output in development
  - Structured format with timestamps, level, module, and message
"""
import sys
from pathlib import Path
from loguru import logger


def setup_logging():
    """Configure Loguru sinks: console + rotating daily file + error file."""

    # Remove the default Loguru sink so we control all output
    logger.remove()

    # --- Console sink (stdout) ---
    # Colored, human-readable output during development
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
            "<level>{message}</level>"
        ),
        backtrace=True,
        diagnose=True,
    )

    # --- Daily rotating general log file ---
    # Rotates at midnight, keeps 30 days of logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger.add(
        logs_dir / "app-{time:YYYY-MM-DD}.log",
        level="INFO",
        rotation="00:00",          # Rotate at midnight
        retention="30 days",       # Keep 30 days of logs
        compression="zip",         # Compress old logs
        encoding="utf-8",
        enqueue=True,              # Thread-safe async writes
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} — {message}"
        ),
        backtrace=True,
        diagnose=False,            # Don't expose variable values in production files
    )

    # --- Dedicated error log file ---
    # Only ERROR and CRITICAL — kept for 7 days
    logger.add(
        logs_dir / "errors.log",
        level="ERROR",
        rotation="100 MB",         # Also rotate if it gets large
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        enqueue=True,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} — {message}\n"
            "{exception}"
        ),
        backtrace=True,
        diagnose=False,
    )

    return logger
