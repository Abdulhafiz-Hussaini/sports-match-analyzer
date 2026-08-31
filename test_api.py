from sports_api_client import SportsAPIClient
from exceptions import SportsAPIError, TeamNotFoundError


client = SportsAPIClient()

# Start with an empty list so the variable always exists
teams = []


# ---------------------------------------------------------
# TEST 1: SEARCH TEAM
# ---------------------------------------------------------

print("=" * 50)
print("TEST 1: SEARCHING FOR ARSENAL")
print("=" * 50)

try:
    teams = client.search_team("Arsenal")

    print(f"Found {len(teams)} team(s).\n")

    for team in teams[:5]:
        print("Team ID:", team.team_id)
        print("Name:", team.name)
        print("Sport:", team.sport)
        print("League:", team.league)
        print("Country:", team.country)
        print("-" * 30)

except TeamNotFoundError as error:
    print("Team error:", error)

except SportsAPIError as error:
    print("API error:", error)


# ---------------------------------------------------------
# TEST 2: UPCOMING MATCHES
# ---------------------------------------------------------

if teams:

    team = teams[0]

    print("\n")
    print("=" * 50)
    print(f"TEST 2: UPCOMING MATCHES FOR {team.name}")
    print("=" * 50)

    try:
        upcoming = client.get_next_events(team.team_id)

        if not upcoming:
            print("No upcoming matches found.")

        else:
            for match in upcoming[:5]:
                print(match.display_name())
                print("Date:", match.date)
                print("Status:", match.status)
                print("Venue:", match.venue)
                print("-" * 30)

    except SportsAPIError as error:
        print("API error:", error)


# ---------------------------------------------------------
# TEST 3: PREVIOUS RESULTS
# ---------------------------------------------------------

if teams:

    print("\n")
    print("=" * 50)
    print(f"TEST 3: RECENT RESULTS FOR {team.name}")
    print("=" * 50)

    try:
        recent = client.get_last_events(team.team_id)

        if not recent:
            print("No recent results found.")

        else:
            for match in recent[:5]:
                print(match.display_name())
                print("Date:", match.date)
                print("Score:", match.score)
                print(
                    f"{team.name}:",
                    match.result_for_team(team.name)
                )
                print("-" * 30)

    except SportsAPIError as error:
        print("API error:", error)


# ---------------------------------------------------------
# TEST 4: INVALID TEAM
# ---------------------------------------------------------

print("\n")
print("=" * 50)
print("TEST 4: INVALID TEAM")
print("=" * 50)

try:
    client.search_team(
        "ThisTeamDefinitelyDoesNotExist123456"
    )

except TeamNotFoundError as error:
    print("Correctly handled:")
    print(error)

except SportsAPIError as error:
    print("API error:", error)