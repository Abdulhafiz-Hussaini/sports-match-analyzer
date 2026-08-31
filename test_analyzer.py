from match import Match
from match_analyzer import MatchAnalyzer


# =========================================================
# ARSENAL RECENT RESULTS
# =========================================================

arsenal_matches = [

    Match(
        "1",
        "Arsenal",
        "Chelsea",
        "2026-08-20",
        home_score=3,
        away_score=1
    ),

    Match(
        "2",
        "Liverpool",
        "Arsenal",
        "2026-08-16",
        home_score=2,
        away_score=2
    ),

    Match(
        "3",
        "Arsenal",
        "Newcastle",
        "2026-08-10",
        home_score=2,
        away_score=0
    ),

    Match(
        "4",
        "Manchester City",
        "Arsenal",
        "2026-08-03",
        home_score=1,
        away_score=0
    ),

    Match(
        "5",
        "Arsenal",
        "Everton",
        "2026-07-27",
        home_score=2,
        away_score=1
    )
]


# =========================================================
# CHELSEA RECENT RESULTS
# =========================================================

chelsea_matches = [

    Match(
        "6",
        "Chelsea",
        "Liverpool",
        "2026-08-20",
        home_score=1,
        away_score=2
    ),

    Match(
        "7",
        "Chelsea",
        "Newcastle",
        "2026-08-16",
        home_score=2,
        away_score=2
    ),

    Match(
        "8",
        "Everton",
        "Chelsea",
        "2026-08-10",
        home_score=0,
        away_score=1
    ),

    Match(
        "9",
        "Chelsea",
        "West Ham",
        "2026-08-03",
        home_score=3,
        away_score=1
    ),

    Match(
        "10",
        "Manchester City",
        "Chelsea",
        "2026-07-27",
        home_score=2,
        away_score=0
    )
]


# =========================================================
# CREATE ANALYZER
# =========================================================

arsenal_analyzer = MatchAnalyzer(
    "Arsenal"
)


# =========================================================
# TEST 1: FORM ANALYSIS
# =========================================================

print("=" * 55)
print("TEST 1: ARSENAL FORM ANALYSIS")
print("=" * 55)

arsenal_stats = arsenal_analyzer.analyze_form(
    arsenal_matches
)

print("Team:", arsenal_stats["team"])
print("Matches:", arsenal_stats["matches"])
print("Wins:", arsenal_stats["wins"])
print("Draws:", arsenal_stats["draws"])
print("Losses:", arsenal_stats["losses"])
print("Goals scored:", arsenal_stats["goals_scored"])
print("Goals conceded:", arsenal_stats["goals_conceded"])
print("Points:", arsenal_stats["points"])


# =========================================================
# TEST 2: FORM STRING
# =========================================================

print("\n")
print("=" * 55)
print("TEST 2: RECENT FORM")
print("=" * 55)

print(
    "Arsenal form:",
    arsenal_analyzer.form_string(
        arsenal_matches
    )
)


# =========================================================
# TEST 3: SIMPLE PREDICTION
# =========================================================

print("\n")
print("=" * 55)
print("TEST 3: SIMPLE MATCH PREDICTION")
print("=" * 55)

prediction = arsenal_analyzer.predict_match(
    "Chelsea",
    arsenal_matches,
    chelsea_matches
)

print(
    "Prediction:",
    prediction["prediction"]
)

print(
    "Result:",
    prediction["result"]
)

print(
    "Confidence:",
    prediction["confidence"],
    "%"
)

print(
    "Arsenal average:",
    prediction["team_average"]
)

print(
    "Chelsea average:",
    prediction["opponent_average"]
)

print("\nNOTE:")
print(prediction["message"])