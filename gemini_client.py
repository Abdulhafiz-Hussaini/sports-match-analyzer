import os

from dotenv import load_dotenv
from google import genai

from exceptions import GeminiAPIError


class GeminiClient:
    """
    Handles communication with Google's Gemini API.

    Gemini is used to generate:
    - Pre-match previews
    - Post-match summaries
    """

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise GeminiAPIError(
                "GEMINI_API_KEY was not found in the .env file."
            )

        try:
            self.client = genai.Client(
                api_key=api_key
            )

        except Exception as error:
            raise GeminiAPIError(
                f"Could not initialize Gemini: {error}"
            ) from error

    # =========================================================
    # PRE-MATCH PREVIEW
    # =========================================================

    def generate_preview(
        self,
        home_team,
        away_team,
        home_form,
        away_form,
        fixture_date=None,
        venue=None
    ):
        """
        Generate a concise pre-match preview.
        """

        prompt = f"""
You are a football match preview assistant.

Create a concise and beginner-friendly pre-match
preview for the following match:

Home team: {home_team}
Away team: {away_team}
Match date: {fixture_date}
Venue: {venue}

Recent form:
{home_team}: {home_form}
{away_team}: {away_form}

Your response should include:

1. A short overview of the fixture.
2. The recent form of both teams.
3. Key things to watch.
4. A balanced conclusion.

Do not claim to know the future.
Do not present the result as certain.
Do not invent statistics.

Keep the preview concise and suitable for a
sports match analyzer application.
"""

        return self._generate(prompt)

    # =========================================================
    # POST-MATCH SUMMARY
    # =========================================================

    def generate_summary(
        self,
        home_team,
        away_team,
        score,
        fixture_date=None,
        venue=None
    ):
        """
        Generate a concise post-match summary.
        """

        prompt = f"""
You are a football match summary assistant.

Write a concise post-match summary for:

Home team: {home_team}
Away team: {away_team}
Final score: {score}
Date: {fixture_date}
Venue: {venue}

The summary should:

1. State the final result.
2. Explain the result in simple football language.
3. Mention the winning team's performance.
4. Mention something about the losing team if applicable.
5. Remain factual based only on the information provided.

Do not invent statistics, scorers, injuries,
possession, or events that were not provided.

Keep the summary concise.
"""

        return self._generate(prompt)

    # =========================================================
    # GEMINI INTERACTIONS API
    # =========================================================

    def _generate(self, prompt):
        """
        Send a request through Gemini's Interactions API.
        """

        try:
            interaction = self.client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            if not interaction:
                raise GeminiAPIError(
                    "Gemini returned no interaction."
                )

            response_text = interaction.output_text

            if not response_text:
                raise GeminiAPIError(
                    "Gemini returned an empty response."
                )

            return response_text.strip()

        except GeminiAPIError:
            raise

        except Exception as error:
            raise GeminiAPIError(
                f"Gemini request failed: {error}"
            ) from error