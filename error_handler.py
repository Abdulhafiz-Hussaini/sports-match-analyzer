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
    def log_error(error):
        """
        Print technical information for debugging.
        """

        print(
            f"[ERROR] "
            f"{type(error).__name__}: "
            f"{error}"
        )