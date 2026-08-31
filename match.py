import re
from datetime import datetime

from exceptions import DataValidationError


class Match:
    """Represents a sports match or fixture."""

    SCORE_PATTERN = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")

    def __init__(
        self,
        match_id,
        home_team,
        away_team,
        date=None,
        home_score=None,
        away_score=None,
        status=None,
        venue=None
    ):
        self.match_id = str(match_id).strip()
        self.home_team = self.clean_text(home_team)
        self.away_team = self.clean_text(away_team)
        self.date = self.parse_date(date)
        self.home_score = self.parse_score_value(home_score)
        self.away_score = self.parse_score_value(away_score)
        self.status = self.clean_text(status) or "Unknown"
        self.venue = self.clean_text(venue) or "Unknown"

        self.validate()

    # ---------------------------------------------------------
    # TEXT CLEANING
    # ---------------------------------------------------------

    @staticmethod
    def clean_text(value):
        """Remove unnecessary whitespace from text."""

        if value is None:
            return ""

        value = str(value)

        return re.sub(r"\s+", " ", value).strip()

    # ---------------------------------------------------------
    # SCORE HANDLING
    # ---------------------------------------------------------

    @classmethod
    def parse_score(cls, score):
        """
        Convert a score such as '2-1' into (2, 1).
        """

        if score is None:
            return None, None

        match = cls.SCORE_PATTERN.fullmatch(str(score))

        if not match:
            raise DataValidationError(
                f"Invalid score format: {score}"
            )

        home_score = int(match.group(1))
        away_score = int(match.group(2))

        return home_score, away_score

    @staticmethod
    def parse_score_value(value):
        """Safely convert an individual score to an integer."""

        if value is None or value == "":
            return None

        try:
            value = int(value)
        except (ValueError, TypeError):
            raise DataValidationError(
                f"Invalid score value: {value}"
            )

        if value < 0:
            raise DataValidationError(
                "A match score cannot be negative."
            )

        return value

    # ---------------------------------------------------------
    # DATE HANDLING
    # ---------------------------------------------------------

    @staticmethod
    def parse_date(date_value):
        """
        Convert a date/time string into a Python datetime object.
        """

        if not date_value:
            return None

        if isinstance(date_value, datetime):
            return date_value

        date_value = str(date_value).strip()

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z"
        ]

        for date_format in formats:
            try:
                return datetime.strptime(date_value, date_format)
            except ValueError:
                continue

        raise DataValidationError(
            f"Invalid date format: {date_value}"
        )

    # ---------------------------------------------------------
    # API CONVERSION
    # ---------------------------------------------------------

    @classmethod
    def from_api_dict(cls, data):
        """
        Create a Match object from TheSportsDB API data.
        """

        if not isinstance(data, dict):
            raise DataValidationError(
                "Match data must be a dictionary."
            )

        match_id = data.get("idEvent")
        home_team = data.get("strHomeTeam")
        away_team = data.get("strAwayTeam")

        if not match_id:
            raise DataValidationError(
                "API response is missing the match ID."
            )

        if not home_team or not away_team:
            raise DataValidationError(
                "API response is missing a home or away team."
            )

        return cls(
            match_id=match_id,
            home_team=home_team,
            away_team=away_team,
            date=cls.combine_api_date_time(data),
            home_score=data.get("intHomeScore"),
            away_score=data.get("intAwayScore"),
            status=data.get("strStatus"),
            venue=data.get("strVenue")
        )

    @staticmethod
    def combine_api_date_time(data):
        """
        Combine TheSportsDB's date and time fields.
        """

        event_date = data.get("dateEvent")
        event_time = data.get("strTime")

        if not event_date:
            return None

        if event_time:
            # The API time may contain timezone information.
            event_time = str(event_time).split("+")[0]

            if len(event_time) >= 8:
                event_time = event_time[:8]

            return f"{event_date} {event_time}"

        return event_date

    # ---------------------------------------------------------
    # MATCH INFORMATION
    # ---------------------------------------------------------

    @property
    def is_finished(self):
        """Return True if a final score is available."""

        return (
            self.home_score is not None
            and self.away_score is not None
        )

    @property
    def score(self):
        """Return the score as a string."""

        if not self.is_finished:
            return "Not played"

        return f"{self.home_score}-{self.away_score}"

    def result_for_team(self, team_name):
        """
        Return Win, Draw or Loss for a particular team.
        """

        if not self.is_finished:
            return "Not played"

        team_name = self.clean_text(team_name).lower()

        home_team = self.home_team.lower()
        away_team = self.away_team.lower()

        if team_name == home_team:
            if self.home_score > self.away_score:
                return "Win"
            elif self.home_score < self.away_score:
                return "Loss"
            return "Draw"

        if team_name == away_team:
            if self.away_score > self.home_score:
                return "Win"
            elif self.away_score < self.home_score:
                return "Loss"
            return "Draw"

        return "Team not involved"

    def display_name(self):
        """Return a user-friendly match name."""

        return f"{self.home_team} vs {self.away_team}"

    def validate(self):
        """Validate essential match information."""

        if not self.match_id:
            raise DataValidationError(
                "Match ID cannot be empty."
            )

        if not self.home_team:
            raise DataValidationError(
                "Home team cannot be empty."
            )

        if not self.away_team:
            raise DataValidationError(
                "Away team cannot be empty."
            )

        if self.home_team.lower() == self.away_team.lower():
            raise DataValidationError(
                "Home and away teams cannot be the same."
            )

    def __str__(self):
        return f"{self.display_name()} ({self.score})"

    def __repr__(self):
        return (
            f"Match("
            f"match_id='{self.match_id}', "
            f"home_team='{self.home_team}', "
            f"away_team='{self.away_team}', "
            f"score='{self.score}'"
            f")"
        )