import json
import os

from exceptions import StorageError


class StorageManager:
    """
    Handles local storage of favourite teams,
    match notes and generated summaries.
    """

    def __init__(self, filename="user_data.json"):
        self.filename = filename

        self.data = {
            "favourite_teams": [],
            "match_notes": {},
            "summaries": {}
        }

        self.load()

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load(self):
        """
        Load user data from the JSON file.

        If the file does not exist, start with empty data.
        If the file is corrupted, raise StorageError.
        """

        if not os.path.exists(self.filename):
            self.save()
            return

        try:
            with open(
                self.filename,
                "r",
                encoding="utf-8"
            ) as file:

                loaded_data = json.load(file)

        except json.JSONDecodeError as error:
            raise StorageError(
                "The user data file contains invalid JSON."
            ) from error

        except OSError as error:
            raise StorageError(
                f"Could not read storage file: {error}"
            ) from error

        if not isinstance(loaded_data, dict):
            raise StorageError(
                "User data must be stored as a JSON object."
            )

        # Preserve our required structure.
        self.data["favourite_teams"] = loaded_data.get(
            "favourite_teams",
            []
        )

        self.data["match_notes"] = loaded_data.get(
            "match_notes",
            {}
        )

        self.data["summaries"] = loaded_data.get(
            "summaries",
            {}
        )

    # =========================================================
    # SAVE DATA
    # =========================================================

    def save(self):
        """
        Save all user data to the JSON file.
        """

        try:
            with open(
                self.filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:
            raise StorageError(
                f"Could not save user data: {error}"
            ) from error

    # =========================================================
    # FAVOURITE TEAMS
    # =========================================================

    def add_favourite_team(self, team):
        """
        Add a team to the user's favourite teams.
        """

        team_data = {
            "team_id": team.team_id,
            "name": team.name,
            "sport": team.sport,
            "league": team.league,
            "country": team.country,
            "badge_url": team.badge_url
        }

        # Prevent duplicate favourites.
        for favourite in self.data["favourite_teams"]:

            if favourite["team_id"] == team.team_id:
                return False

        self.data["favourite_teams"].append(team_data)

        self.save()

        return True

    def remove_favourite_team(self, team_id):
        """
        Remove a team from favourites.
        """

        original_count = len(
            self.data["favourite_teams"]
        )

        self.data["favourite_teams"] = [
            team
            for team in self.data["favourite_teams"]
            if team.get("team_id") != str(team_id)
        ]

        removed = (
            len(self.data["favourite_teams"])
            < original_count
        )

        if removed:
            self.save()

        return removed

    def get_favourite_teams(self):
        """
        Return all favourite teams.
        """

        return self.data["favourite_teams"]

    def is_favourite(self, team_id):
        """
        Check whether a team is already a favourite.
        """

        return any(
            team.get("team_id") == str(team_id)
            for team in self.data["favourite_teams"]
        )

    # =========================================================
    # MATCH NOTES
    # =========================================================

    def save_match_note(self, match_id, note):
        """
        Save a note for a specific match.
        """

        match_id = str(match_id)

        if not note or not str(note).strip():
            raise StorageError(
                "Match note cannot be empty."
            )

        self.data["match_notes"][match_id] = {
            "note": str(note).strip()
        }

        self.save()

    def get_match_note(self, match_id):
        """
        Retrieve a note for a specific match.
        """

        match_id = str(match_id)

        note_data = self.data["match_notes"].get(
            match_id
        )

        if not note_data:
            return None

        return note_data.get("note")

    def delete_match_note(self, match_id):
        """
        Delete a note associated with a match.
        """

        match_id = str(match_id)

        if match_id not in self.data["match_notes"]:
            return False

        del self.data["match_notes"][match_id]

        self.save()

        return True

    # =========================================================
    # GENERATED SUMMARIES
    # =========================================================

    def save_summary(self, match_id, summary):
        """
        Save an AI-generated or manually generated
        summary for a specific match.
        """

        match_id = str(match_id)

        if not summary or not str(summary).strip():
            raise StorageError(
                "Summary cannot be empty."
            )

        self.data["summaries"][match_id] = {
            "summary": str(summary).strip()
        }

        self.save()

    def get_summary(self, match_id):
        """
        Retrieve a saved summary for a match.
        """

        match_id = str(match_id)

        summary_data = self.data["summaries"].get(
            match_id
        )

        if not summary_data:
            return None

        return summary_data.get("summary")

    def delete_summary(self, match_id):
        """
        Delete a saved summary.
        """

        match_id = str(match_id)

        if match_id not in self.data["summaries"]:
            return False

        del self.data["summaries"][match_id]

        self.save()

        return True

    # =========================================================
    # CLEAR ALL DATA
    # =========================================================

    def clear_all(self):
        """
        Delete all locally stored user data.
        """

        self.data = {
            "favourite_teams": [],
            "match_notes": {},
            "summaries": {}
        }

        self.save()