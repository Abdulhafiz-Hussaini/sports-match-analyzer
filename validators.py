from datetime import datetime

import re

from exceptions import ValidationError


class InputValidator:
    """
    Validates user input before it reaches
    the application's core logic.
    """

    # =========================================================
    # TEAM NAME
    # =========================================================

    @staticmethod
    def validate_team_name(team_name):
        """
        Validate a football team name.
        """

        if team_name is None:
            raise ValidationError(
                "Team name cannot be empty."
            )

        team_name = str(team_name).strip()

        if not team_name:
            raise ValidationError(
                "Team name cannot be empty."
            )

        if len(team_name) < 2:
            raise ValidationError(
                "Team name must contain at least 2 characters."
            )

        if len(team_name) > 100:
            raise ValidationError(
                "Team name is too long."
            )

        # Allow letters, numbers, spaces and common
        # football team punctuation.
        if not re.match(
            r"^[A-Za-z0-9À-ÿ .'\-&]+$",
            team_name
        ):
            raise ValidationError(
                "Team name contains invalid characters."
            )

        return team_name

    # =========================================================
    # MATCH ID
    # =========================================================

    @staticmethod
    def validate_match_id(match_id):
        """
        Validate a match ID.
        """

        if match_id is None:
            raise ValidationError(
                "Match ID cannot be empty."
            )

        match_id = str(match_id).strip()

        if not match_id:
            raise ValidationError(
                "Match ID cannot be empty."
            )

        if not match_id.isdigit():
            raise ValidationError(
                "Match ID must contain only numbers."
            )

        return match_id

    # =========================================================
    # NOTE
    # =========================================================

    @staticmethod
    def validate_note(note):
        """
        Validate a user's match note.
        """

        if note is None:
            raise ValidationError(
                "Note cannot be empty."
            )

        note = str(note).strip()

        if not note:
            raise ValidationError(
                "Note cannot be empty."
            )

        if len(note) > 1000:
            raise ValidationError(
                "Note cannot exceed 1000 characters."
            )

        return note

    # =========================================================
    # SCORE
    # =========================================================

    @staticmethod
    def validate_score(score):
        """
        Validate a football score such as 3-1.
        """

        if score is None:
            raise ValidationError(
                "Score cannot be empty."
            )

        score = str(score).strip()

        if not re.match(
            r"^\d+\s*-\s*\d+$",
            score
        ):
            raise ValidationError(
                "Invalid score format. Expected something like 3-1."
            )

        return score

    @staticmethod
    def validate_date(date_str):
        """
        Validate a date string in YYYY-MM-DD format.
        """

        if date_str is None:
            raise ValidationError("Date cannot be empty.")

        date_str = str(date_str).strip()

        if not date_str:
            raise ValidationError("Date cannot be empty.")

        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",date_str):
            raise ValidationError("Invalid date format. Expected YYYY-MM-DD format.")

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(f"'{date_str}' is not a real calendar date.")

        return date_str

