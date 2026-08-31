import requests

from team import Team
from match import Match
from exceptions import (
    SportsAPIError,
    TeamNotFoundError,
    DataValidationError
)
from validators import InputValidator


class SportsAPIClient:
    """Client for communicating with TheSportsDB API."""

    BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"

    def __init__(self, timeout=10):
        self.timeout = timeout

    # ---------------------------------------------------------
    # INTERNAL REQUEST METHOD
    # ---------------------------------------------------------

    def _get(self, endpoint, params=None):
        """
        Send a GET request to TheSportsDB API.
        """

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

        except requests.exceptions.Timeout as error:
            raise SportsAPIError(
                "The sports API request timed out."
            ) from error

        except requests.exceptions.ConnectionError as error:
            raise SportsAPIError(
                "Could not connect to the sports API."
            ) from error

        except requests.exceptions.HTTPError as error:
            raise SportsAPIError(
                f"The sports API returned an HTTP error: "
                f"{response.status_code}"
            ) from error

        except requests.exceptions.RequestException as error:
            raise SportsAPIError(
                f"Sports API request failed: {error}"
            ) from error

        try:
            data = response.json()

        except ValueError as error:
            raise SportsAPIError(
                "The sports API returned invalid JSON data."
            ) from error

        if not isinstance(data, dict):
            raise SportsAPIError(
                "Unexpected response format from the sports API."
            )

        return data

    # ---------------------------------------------------------
    # TEAM SEARCH
    # ---------------------------------------------------------

    def search_team(self, team_name):
        """
        Search for a team and return a list of Team objects.
        """

        # Validate user input before contacting the API.
        team_name = InputValidator.validate_team_name(
            team_name
        )

        data = self._get(
            "searchteams.php",
            params={"t": team_name}
        )

        teams_data = data.get("teams")

        if not teams_data:
            raise TeamNotFoundError(
                f"No team was found for '{team_name}'."
            )

        teams = []

        for team_data in teams_data:

            try:
                team = Team.from_api_dict(team_data)
                teams.append(team)

            except Exception:
                # Ignore malformed individual team records
                # instead of crashing the entire search.
                continue

        if not teams:
            raise TeamNotFoundError(
                f"No valid team data was found for '{team_name}'."
            )

        return teams

    # ---------------------------------------------------------
    # UPCOMING FIXTURES
    # ---------------------------------------------------------

    def get_next_events(self, team_id):
        """
        Get upcoming matches for a team.
        """

        if not team_id:
            raise SportsAPIError(
                "A valid team ID is required."
            )

        data = self._get(
            "eventsnext.php",
            params={"id": team_id}
        )

        events = data.get("events") or []

        matches = []

        for event in events:

            try:
                match = Match.from_api_dict(event)
                matches.append(match)

            except Exception:
                # Ignore invalid match records.
                continue

        return matches

    # ---------------------------------------------------------
    # PREVIOUS RESULTS
    # ---------------------------------------------------------

    def get_last_events(self, team_id):
        """
        Get previous matches/results for a team.
        """

        if not team_id:
            raise SportsAPIError(
                "A valid team ID is required."
            )

        data = self._get(
            "eventslast.php",
            params={"id": team_id}
        )

        events = data.get("results") or []

        matches = []

        for event in events:

            try:
                match = Match.from_api_dict(event)
                matches.append(match)

            except DataValidationError:
            # Ignore malformed individual team records
            # instead of crashing the entire search.
                continue

        return matches

    # ---------------------------------------------------------
    # COMBINED TEAM DATA
    # ---------------------------------------------------------

    def get_team_matches(self, team):
        """
        Retrieve both upcoming fixtures and recent results
        for a Team object.
        """

        if not isinstance(team, Team):
            raise TypeError(
                "team must be a Team object."
            )

        upcoming = self.get_next_events(
            team.team_id
        )

        recent = self.get_last_events(
            team.team_id
        )

        return {
            "upcoming": upcoming,
            "recent": recent
        }