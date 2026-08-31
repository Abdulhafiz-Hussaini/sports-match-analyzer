class MatchAnalyzer:
    """
    Performs simple analysis of a team's recent matches
    and provides a basic form-based prediction.
    """

    def __init__(self, team_name):
        self.team_name = team_name.strip()

    # =========================================================
    # FORM ANALYSIS
    # =========================================================

    def analyze_form(self, matches):
        """
        Analyze a team's recent matches.

        Calculates:
        - Wins
        - Draws
        - Losses
        - Goals scored
        - Goals conceded
        - Points
        """

        wins = 0
        draws = 0
        losses = 0

        goals_scored = 0
        goals_conceded = 0

        for match in matches:

            result = match.result_for_team(
                self.team_name
            )

            if result == "Win":
                wins += 1

            elif result == "Draw":
                draws += 1

            elif result == "Loss":
                losses += 1

            # ---------------------------------------------
            # Calculate goals
            # ---------------------------------------------

            if not match.is_finished:
                continue

            team_name = self.team_name.lower()

            home_team = match.home_team.lower()
            away_team = match.away_team.lower()

            if team_name == home_team:

                goals_scored += match.home_score
                goals_conceded += match.away_score

            elif team_name == away_team:

                goals_scored += match.away_score
                goals_conceded += match.home_score

        total_matches = wins + draws + losses

        # Football points:
        # Win = 3
        # Draw = 1
        # Loss = 0

        points = (wins * 3) + draws

        return {
            "team": self.team_name,
            "matches": total_matches,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded,
            "points": points
        }

    # =========================================================
    # FORM STRING
    # =========================================================

    def form_string(self, matches):
        """
        Return recent form such as:

        W W D L W
        """

        form = []

        for match in matches:

            result = match.result_for_team(
                self.team_name
            )

            if result == "Win":
                form.append("W")

            elif result == "Draw":
                form.append("D")

            elif result == "Loss":
                form.append("L")

        return " ".join(form)

    # =========================================================
    # SIMPLE PREDICTION
    # =========================================================

    def predict_match(
        self,
        opponent_name,
        team_matches,
        opponent_matches
    ):
        """
        Provide a simple form-based prediction.

        This is only a fun estimate based on recent
        results. It is NOT a guaranteed prediction.
        """

        team_stats = self.analyze_form(
            team_matches
        )

        opponent_analyzer = MatchAnalyzer(
            opponent_name
        )

        opponent_stats = opponent_analyzer.analyze_form(
            opponent_matches
        )

        # ---------------------------------------------
        # Average points per match
        # ---------------------------------------------

        if team_stats["matches"] > 0:
            team_average = (
                team_stats["points"]
                / team_stats["matches"]
            )
        else:
            team_average = 0

        if opponent_stats["matches"] > 0:
            opponent_average = (
                opponent_stats["points"]
                / opponent_stats["matches"]
            )
        else:
            opponent_average = 0

        difference = (
            team_average - opponent_average
        )

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        if difference > 0.75:

            prediction = self.team_name
            result = "Win"

        elif difference < -0.75:

            prediction = opponent_name
            result = "Win"

        else:

            prediction = "Draw"
            result = "Draw"

        # ---------------------------------------------
        # Confidence
        # ---------------------------------------------

        confidence = min(
            95,
            max(
                50,
                50 + abs(difference) * 25
            )
        )

        return {
            "prediction": prediction,
            "result": result,
            "confidence": round(
                confidence,
                1
            ),
            "team_average": round(
                team_average,
                2
            ),
            "opponent_average": round(
                opponent_average,
                2
            ),
            "message": (
                "Fun estimate based on recent form. "
                "It is not a guaranteed prediction."
            )
        }