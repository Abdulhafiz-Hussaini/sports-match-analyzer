from storage import StorageManager
from team import Team


# =========================================================
# CREATE TEST STORAGE
# =========================================================

storage = StorageManager("test_user_data.json")


# =========================================================
# CREATE TEST TEAM
# =========================================================

team = Team(
    team_id="133604",
    name="Arsenal",
    sport="Soccer",
    league="English Premier League",
    country="England",
    badge_url="https://example.com/arsenal.png"
)


# =========================================================
# TEST 1: ADD FAVOURITE
# =========================================================

print("=" * 50)
print("TEST 1: ADD FAVOURITE TEAM")
print("=" * 50)

added = storage.add_favourite_team(team)

print("Added:", added)
print("Favourites:")
print(storage.get_favourite_teams())


# =========================================================
# TEST 2: DUPLICATE FAVOURITE
# =========================================================

print("\n")
print("=" * 50)
print("TEST 2: DUPLICATE FAVOURITE")
print("=" * 50)

added_again = storage.add_favourite_team(team)

print("Added again:", added_again)


# =========================================================
# TEST 3: MATCH NOTE
# =========================================================

print("\n")
print("=" * 50)
print("TEST 3: SAVE MATCH NOTE")
print("=" * 50)

storage.save_match_note(
    "12345",
    "Important match. Watch the midfield performance."
)

print(
    "Saved note:",
    storage.get_match_note("12345")
)


# =========================================================
# TEST 4: GENERATED SUMMARY
# =========================================================

print("\n")
print("=" * 50)
print("TEST 4: SAVE SUMMARY")
print("=" * 50)

storage.save_summary(
    "12345",
    "Arsenal showed strong attacking performance."
)

print(
    "Saved summary:",
    storage.get_summary("12345")
)


# =========================================================
# TEST 5: CHECK PERSISTENCE
# =========================================================

print("\n")
print("=" * 50)
print("TEST 5: CHECK DATA PERSISTENCE")
print("=" * 50)

new_storage = StorageManager("test_user_data.json")

print(
    "Loaded favourites:",
    new_storage.get_favourite_teams()
)

print(
    "Loaded note:",
    new_storage.get_match_note("12345")
)

print(
    "Loaded summary:",
    new_storage.get_summary("12345")
)


# =========================================================
# TEST 6: DELETE NOTE
# =========================================================

print("\n")
print("=" * 50)
print("TEST 6: DELETE NOTE")
print("=" * 50)

deleted = new_storage.delete_match_note("12345")

print("Deleted:", deleted)
print(
    "Note after deletion:",
    new_storage.get_match_note("12345")
)


# =========================================================
# TEST 7: REMOVE FAVOURITE
# =========================================================

print("\n")
print("=" * 50)
print("TEST 7: REMOVE FAVOURITE")
print("=" * 50)

removed = new_storage.remove_favourite_team("133604")

print("Removed:", removed)

print(
    "Favourites after removal:",
    new_storage.get_favourite_teams()
)