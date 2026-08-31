from gemini_client import GeminiClient
from exceptions import GeminiAPIError


print("=" * 60)
print("GEMINI AI TEST")
print("=" * 60)


try:

    gemini = GeminiClient()

    print("\nGemini client initialized successfully.")
    print("Generating pre-match preview...\n")

    preview = gemini.generate_preview(
        home_team="Arsenal",
        away_team="Chelsea",
        home_form="W W D W L",
        away_form="W D L W W",
        fixture_date="2026-09-01",
        venue="Emirates Stadium"
    )

    print("=" * 60)
    print("PRE-MATCH PREVIEW")
    print("=" * 60)

    print(preview)


except GeminiAPIError as error:

    print("\nGemini error:")
    print(error)


except Exception as error:

    print("\nUnexpected error:")
    print(error)