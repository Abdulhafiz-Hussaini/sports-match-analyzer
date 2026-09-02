from datetime import datetime

from exceptions import (
    SportsAPIError,
    StorageError,
    GeminiAPIError,
    ValidationError
)


class ErrorHandler:
    """
    Converts technical exceptions into
    user-friendly messages.
    """

    @staticmethod
    def get_message(error):
        """
        Return a user-friendly message for an exception.
        """

        if isinstance(error, ValidationError):
            return f"Input error: {error}"

        if isinstance(error, SportsAPIError):
            return (
                "Sports data error: "
                f"{error}"
            )

        if isinstance(error, StorageError):
            return (
                "Storage error: "
                f"{error}"
            )

        if isinstance(error, GeminiAPIError):
            return (
                "AI service error: "
                f"{error}"
            )

        return (
            "An unexpected error occurred. "
            "Please try again."
        )

    @staticmethod
    def log_error(error, log_path = "error_log.txt"):
        """
        Write technical error information to log file.
        """
        try:
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"[{datetime.now()}] {type(error).__name__}: {error}\n")
        except OSError:
            print(f"[ERROR] Could not write to log file: {error}")
