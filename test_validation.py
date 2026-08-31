from validators import InputValidator
from error_handler import ErrorHandler
from exceptions import ValidationError


print("=" * 60)
print("PHASE 7 — VALIDATION & ERROR HANDLING TEST")
print("=" * 60)


# =========================================================
# TEST 1: VALID TEAM
# =========================================================

print("\nTEST 1: Valid team name")

try:

    result = InputValidator.validate_team_name(
        "Arsenal"
    )

    print("PASS:", result)

except ValidationError as error:

    print("FAIL:", ErrorHandler.get_message(error))


# =========================================================
# TEST 2: EMPTY TEAM
# =========================================================

print("\nTEST 2: Empty team name")

try:

    InputValidator.validate_team_name("")

    print("FAIL: Empty team was accepted.")

except ValidationError as error:

    print(
        "PASS:",
        ErrorHandler.get_message(error)
    )


# =========================================================
# TEST 3: INVALID TEAM CHARACTERS
# =========================================================

print("\nTEST 3: Invalid team name")

try:

    InputValidator.validate_team_name(
        "Arsenal!!!###"
    )

    print("FAIL: Invalid input was accepted.")

except ValidationError as error:

    print(
        "PASS:",
        ErrorHandler.get_message(error)
    )


# =========================================================
# TEST 4: VALID SCORE
# =========================================================

print("\nTEST 4: Valid score")

try:

    result = InputValidator.validate_score(
        "3-1"
    )

    print("PASS:", result)

except ValidationError as error:

    print("FAIL:", ErrorHandler.get_message(error))


# =========================================================
# TEST 5: INVALID SCORE
# =========================================================

print("\nTEST 5: Invalid score")

try:

    InputValidator.validate_score(
        "three-one"
    )

    print("FAIL: Invalid score was accepted.")

except ValidationError as error:

    print(
        "PASS:",
        ErrorHandler.get_message(error)
    )


# =========================================================
# TEST 6: EMPTY NOTE
# =========================================================

print("\nTEST 6: Empty match note")

try:

    InputValidator.validate_note("")

    print("FAIL: Empty note was accepted.")

except ValidationError as error:

    print(
        "PASS:",
        ErrorHandler.get_message(error)
    )


# =========================================================
# TEST 7: VALID MATCH ID
# =========================================================

print("\nTEST 7: Valid match ID")

try:

    result = InputValidator.validate_match_id(
        "12345"
    )

    print("PASS:", result)

except ValidationError as error:

    print("FAIL:", ErrorHandler.get_message(error))


# =========================================================
# TEST 8: INVALID MATCH ID
# =========================================================

print("\nTEST 8: Invalid match ID")

try:

    InputValidator.validate_match_id(
        "ABC123"
    )

    print("FAIL: Invalid match ID was accepted.")

except ValidationError as error:

    print(
        "PASS:",
        ErrorHandler.get_message(error)
    )


# =========================================================
# COMPLETE
# =========================================================

print("\n" + "=" * 60)
print("PHASE 7 TEST COMPLETE")
print("=" * 60)