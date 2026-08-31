import re

from exceptions import DataValidationError


class Team:
    """Represents a sports team."""

    def __init__(
        self,
        team_id,
        name,
        sport=None,
        league=None,
        country=None,
        badge_url=None
    ):
        self.team_id = str(team_id).strip()
        self.name = self.clean_name(name)
        self.sport = self.clean_name(sport) if sport else "Unknown"
        self.league = self.clean_name(league) if league else "Unknown"
        self.country = self.clean_name(country) if country else "Unknown"
        self.badge_url = badge_url

        self.validate()

    @staticmethod
    def clean_name(name):
        """
        Clean unnecessary whitespace from a team name.
        """
        if name is None:
            return ""

        name = str(name)

        # Replace multiple spaces/tabs/newlines with one space
        name = re.sub(r"\s+", " ", name)

        return name.strip()

    def validate(self):
        """Validate essential team information."""

        if not self.team_id:
            raise DataValidationError("Team ID cannot be empty.")

        if not self.name:
            raise DataValidationError("Team name cannot be empty.")

    @classmethod
    def from_api_dict(cls, data):
        """
        Create a Team object from TheSportsDB API data.
        """

        if not isinstance(data, dict):
            raise DataValidationError("Team data must be a dictionary.")

        team_id = data.get("idTeam")
        name = data.get("strTeam")

        if not team_id or not name:
            raise DataValidationError(
                "API response is missing the team's ID or name."
            )

        return cls(
            team_id=team_id,
            name=name,
            sport=data.get("strSport"),
            league=data.get("strLeague"),
            country=data.get("strCountry"),
            badge_url=data.get("strBadge")
        )

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"Team("
            f"team_id='{self.team_id}', "
            f"name='{self.name}', "
            f"sport='{self.sport}', "
            f"league='{self.league}'"
            f")"
        )