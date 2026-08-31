class SportsAPIError(Exception):
    """Base exception for sports API errors."""
    pass


class TeamNotFoundError(SportsAPIError):
    """Raised when a team cannot be found."""
    pass


class MatchNotFoundError(SportsAPIError):
    """Raised when a match cannot be found."""
    pass


class InvalidAPIResponseError(SportsAPIError):
    """Raised when the sports API returns invalid data."""
    pass


class StorageError(Exception):
    """Raised when local storage operations fail."""
    pass


class GeminiAPIError(Exception):
    """Raised when Gemini API operations fail."""
    pass


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


class DataValidationError(ValidationError):
    """
    Raised when data fails model-level validation.

    This is kept separate from user input validation so
    Team and Match objects can report invalid API data.
    """
    pass