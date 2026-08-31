from team import Team
from match import Match


# ---------------------------------------------------------
# TEST TEAM
# ---------------------------------------------------------

team_data = {
    "idTeam": "133604",
    "strTeam": "   Arsenal     ",
    "strSport": "Soccer",
    "strLeague": "English Premier League",
    "strCountry": "England",
    "strBadge": "https://example.com/arsenal.png"
}

team = Team.from_api_dict(team_data)

print("TEAM TEST")
print("--------------------")
print("Name:", team.name)
print("Sport:", team.sport)
print("League:", team.league)
print("Country:", team.country)
print("Object:", team)


# ---------------------------------------------------------
# TEST MATCH
# ---------------------------------------------------------

match_data = {
    "idEvent": "12345",
    "strHomeTeam": "Arsenal",
    "strAwayTeam": "Chelsea",
    "dateEvent": "2026-08-30",
    "strTime": "18:30:00",
    "intHomeScore": 2,
    "intAwayScore": 1,
    "strStatus": "Match Finished",
    "strVenue": "Emirates Stadium"
}

match = Match.from_api_dict(match_data)

print("\nMATCH TEST")
print("--------------------")
print("Match:", match.display_name())
print("Date:", match.date)
print("Score:", match.score)
print("Finished:", match.is_finished)

print("\nRESULT TEST")
print("--------------------")
print("Arsenal:", match.result_for_team("Arsenal"))
print("Chelsea:", match.result_for_team("Chelsea"))