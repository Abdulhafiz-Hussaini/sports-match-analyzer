import streamlit as st

from sports_api_client import SportsAPIClient
from storage import StorageManager
from match_analyzer import MatchAnalyzer
from gemini_client import GeminiClient

from exceptions import (
    SportsAPIError,
    StorageError,
    GeminiAPIError,
    ValidationError
)

from validators import InputValidator
from error_handler import ErrorHandler


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sports Match Analyzer",
    page_icon="⚽",
    layout="wide"
)


# =========================================================
# APPLICATION SERVICES
# =========================================================

@st.cache_resource
def get_api_client():
    return SportsAPIClient()


@st.cache_resource
def get_gemini_client():
    try:
        return GeminiClient()
    except GeminiAPIError:
        return None


@st.cache_resource
def get_storage():
    return StorageManager()


api_client = get_api_client()
storage = get_storage()
gemini = get_gemini_client()


# =========================================================
# SESSION STATE
# =========================================================

if "selected_team" not in st.session_state:
    st.session_state.selected_team = None

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "recent_matches" not in st.session_state:
    st.session_state.recent_matches = []

if "upcoming_matches" not in st.session_state:
    st.session_state.upcoming_matches = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def show_error(error):
    """
    Log an error and display a user-friendly message.
    """
    ErrorHandler.log_error(error)
    st.error(ErrorHandler.get_message(error))


def load_team_matches(team):
    """
    Load recent and upcoming matches for a team.
    """

    recent = api_client.get_last_events(
        team.team_id
    )

    upcoming = api_client.get_next_events(
        team.team_id
    )

    return recent, upcoming


def find_opponent_team(opponent_name):
    """
    Search for an opponent and return the first
    valid Team object.
    """

    results = api_client.search_team(
        opponent_name
    )

    if not results:
        raise SportsAPIError(
            f"Could not find opponent: {opponent_name}"
        )

    return results[0]


# =========================================================
# HEADER
# =========================================================

st.title("⚽ Sports Match Analyzer")

st.markdown(
    """
Welcome to **Sports Match Analyzer** — a football companion
for searching teams, checking fixtures, analysing recent
form, predicting match outcomes, saving favourites,
writing match notes and generating AI-powered insights.
"""
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Navigation")

    page = st.radio(
        "Choose a section:",
        [
            "🔎 Team Search",
            "⭐ Favourites"
        ]
    )

    st.divider()

    st.caption(
        "Sports data powered by TheSportsDB"
    )

    st.caption(
        "AI insights powered by Gemini"
    )


# =========================================================
# TEAM SEARCH PAGE
# =========================================================

if page == "🔎 Team Search":

    st.header("🔎 Search for a Team")

    search_col, button_col = st.columns(
        [4, 1]
    )

    with search_col:

        team_name = st.text_input(
            "Team name",
            placeholder="e.g. Arsenal"
        )

    with button_col:

        st.write("")

        search_button = st.button(
            "Search",
            type="primary",
            use_container_width=True
        )

    # =====================================================
    # SEARCH
    # =====================================================

    if search_button:

        try:

            validated_name = (
                InputValidator.validate_team_name(
                    team_name
                )
            )

            with st.spinner(
                "Searching sports database..."
            ):

                teams = api_client.search_team(
                    validated_name
                )

            st.session_state.search_results = teams

            if teams:

                st.success(
                    f"Found {len(teams)} team(s)."
                )

        except (
            ValidationError,
            SportsAPIError
        ) as error:

            show_error(error)

    # =====================================================
    # SEARCH RESULTS
    # =====================================================

    teams = st.session_state.search_results

    if teams:

        st.subheader("Search Results")

        for team in teams:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.subheader(
                        team.name
                    )

                    st.write(
                        f"**Sport:** {team.sport}"
                    )

                    st.write(
                        f"**League:** {team.league}"
                    )

                    st.write(
                        f"**Country:** {team.country}"
                    )

                with col2:

                    if st.button(
                        "View Team",
                        key=f"view_{team.team_id}"
                    ):

                        st.session_state.selected_team = team

                        st.session_state.recent_matches = []

                        st.session_state.upcoming_matches = []

                        st.rerun()

    # =====================================================
    # SELECTED TEAM
    # =====================================================

    selected_team = st.session_state.selected_team

    if selected_team:

        st.divider()

        st.header(
            f"⚽ {selected_team.name}"
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.metric(
                "Sport",
                selected_team.sport
            )

        with info2:

            st.metric(
                "League",
                selected_team.league
            )

        with info3:

            st.metric(
                "Country",
                selected_team.country
            )

        # =================================================
        # TEAM BADGE
        # =================================================

        if selected_team.badge_url:

            st.image(
                selected_team.badge_url,
                width=120
            )

        # =================================================
        # FAVOURITE
        # =================================================

        st.subheader("⭐ Favourite Team")

        if storage.is_favourite(
            selected_team.team_id
        ):

            st.success(
                "This team is already in your favourites."
            )

        else:

            if st.button(
                "⭐ Add to Favourites"
            ):

                try:

                    added = (
                        storage.add_favourite_team(
                            selected_team
                        )
                    )

                    if added:

                        st.success(
                            f"{selected_team.name} "
                            "added to favourites!"
                        )

                    else:

                        st.info(
                            "This team is already a favourite."
                        )

                except StorageError as error:

                    show_error(error)

        # =================================================
        # LOAD MATCH DATA
        # =================================================

        st.subheader("📊 Match Data")

        if st.button(
            "📊 Load Match Analysis",
            type="primary"
        ):

            try:

                with st.spinner(
                    "Loading match data..."
                ):

                    recent, upcoming = (
                        load_team_matches(
                            selected_team
                        )
                    )

                st.session_state.recent_matches = recent

                st.session_state.upcoming_matches = upcoming

                st.success(
                    "Match data loaded successfully."
                )

            except SportsAPIError as error:

                show_error(error)

        recent_matches = (
            st.session_state.recent_matches
        )

        upcoming_matches = (
            st.session_state.upcoming_matches
        )

        # =================================================
        # ANALYSIS
        # =================================================

        if recent_matches:

            analyzer = MatchAnalyzer(
                selected_team.name
            )

            stats = analyzer.analyze_form(
                recent_matches
            )

            form = analyzer.form_string(
                recent_matches
            )

            # =============================================
            # RECENT FORM
            # =============================================

            st.subheader(
                "📈 Recent Form"
            )

            st.write(
                f"**Form:** `{form}`"
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "Wins",
                    stats["wins"]
                )

            with c2:

                st.metric(
                    "Draws",
                    stats["draws"]
                )

            with c3:

                st.metric(
                    "Losses",
                    stats["losses"]
                )

            with c4:

                st.metric(
                    "Points",
                    stats["points"]
                )

            g1, g2 = st.columns(2)

            with g1:

                st.metric(
                    "Goals Scored",
                    stats["goals_scored"]
                )

            with g2:

                st.metric(
                    "Goals Conceded",
                    stats["goals_conceded"]
                )

            # =============================================
            # RECENT RESULTS
            # =============================================

            st.subheader(
                "🕘 Recent Results"
            )

            for match in recent_matches[:5]:

                result = (
                    match.result_for_team(
                        selected_team.name
                    )
                )

                with st.container(
                    border=True
                ):

                    st.write(
                        f"**{match.display_name()}**"
                    )

                    st.write(
                        f"Score: **{match.score or 'N/A'}**"
                    )

                    st.write(
                        f"Result: **{result}**"
                    )

                    st.caption(
                        f"Date: {match.date} | "
                        f"Venue: {match.venue or 'N/A'}"
                    )

                    # =====================================
                    # MATCH NOTE
                    # =====================================

                    note = storage.get_match_note(
                        match.match_id
                    )

                    with st.expander(
                        "📝 Match Note"
                    ):

                        note_value = st.text_area(
                            "Your note",
                            value=note or "",
                            key=f"note_{match.match_id}"
                        )

                        note_col1, note_col2 = (
                            st.columns(2)
                        )

                        with note_col1:

                            if st.button(
                                "💾 Save Note",
                                key=f"save_note_{match.match_id}"
                            ):

                                try:

                                    storage.save_match_note(
                                        match.match_id,
                                        note_value
                                    )

                                    st.success(
                                        "Note saved."
                                    )

                                except StorageError as error:

                                    show_error(error)

                        with note_col2:

                            if note:

                                if st.button(
                                    "🗑️ Delete Note",
                                    key=f"delete_note_{match.match_id}"
                                ):

                                    try:

                                        storage.delete_match_note(
                                            match.match_id
                                        )

                                        st.success(
                                            "Note deleted."
                                        )

                                        st.rerun()

                                    except StorageError as error:

                                        show_error(error)

        else:

            st.info(
                "Load match analysis to see recent form."
            )

        # =================================================
        # UPCOMING FIXTURES
        # =================================================

        if upcoming_matches:

            st.divider()

            st.subheader(
                "📅 Upcoming Fixtures"
            )

            for index, match in enumerate(
                upcoming_matches[:5]
            ):

                with st.container(
                    border=True
                ):

                    st.write(
                        f"### ⚽ {match.display_name()}"
                    )

                    st.write(
                        f"**Date:** {match.date}"
                    )

                    st.write(
                        f"**Venue:** "
                        f"{match.venue or 'N/A'}"
                    )

                    # =====================================
                    # UPCOMING MATCH NOTE
                    # =====================================

                    existing_note = (
                        storage.get_match_note(
                            match.match_id
                        )
                    )

                    with st.expander(
                        "📝 Add / View Match Note"
                    ):

                        upcoming_note = st.text_area(
                            "Match note",
                            value=existing_note or "",
                            key=f"upcoming_note_{match.match_id}"
                        )

                        save_note_col, delete_note_col = (
                            st.columns(2)
                        )

                        with save_note_col:

                            if st.button(
                                "💾 Save Note",
                                key=f"up_save_{match.match_id}"
                            ):

                                try:

                                    storage.save_match_note(
                                        match.match_id,
                                        upcoming_note
                                    )

                                    st.success(
                                        "Match note saved."
                                    )

                                except StorageError as error:

                                    show_error(error)

                        with delete_note_col:

                            if existing_note:

                                if st.button(
                                    "🗑️ Delete Note",
                                    key=f"up_delete_{match.match_id}"
                                ):

                                    try:

                                        storage.delete_match_note(
                                            match.match_id
                                        )

                                        st.success(
                                            "Match note deleted."
                                        )

                                        st.rerun()

                                    except StorageError as error:

                                        show_error(error)

            # =================================================
            # PREDICTION
            # =================================================

            st.divider()

            st.subheader(
                "🔮 Form-Based Prediction"
            )

            first_match = upcoming_matches[0]

            if (
                first_match.home_team.lower()
                == selected_team.name.lower()
            ):

                opponent_name = (
                    first_match.away_team
                )

            else:

                opponent_name = (
                    first_match.home_team
                )

            st.write(
                f"Next fixture: "
                f"**{first_match.home_team}** vs "
                f"**{first_match.away_team}**"
            )

            if recent_matches:

                if st.button(
                    "🔮 Analyze Match",
                    type="secondary"
                ):

                    try:

                        with st.spinner(
                            "Comparing recent form..."
                        ):

                            opponent_team = (
                                find_opponent_team(
                                    opponent_name
                                )
                            )

                            opponent_matches = (
                                api_client.get_last_events(
                                    opponent_team.team_id
                                )
                            )

                            prediction = (
                                analyzer.predict_match(
                                    opponent_name,
                                    recent_matches,
                                    opponent_matches
                                )
                            )

                        st.session_state[
                            "prediction"
                        ] = prediction

                    except (
                        SportsAPIError,
                        ValidationError
                    ) as error:

                        show_error(error)

                prediction = st.session_state.get(
                    "prediction"
                )

                if prediction:

                    p1, p2, p3 = st.columns(3)

                    with p1:

                        st.metric(
                            "Prediction",
                            prediction["prediction"]
                        )

                    with p2:

                        st.metric(
                            "Expected Result",
                            prediction["result"]
                        )

                    with p3:

                        st.metric(
                            "Confidence",
                            f"{prediction['confidence']}%"
                        )

                    a1, a2 = st.columns(2)

                    with a1:

                        st.write(
                            f"**{selected_team.name} "
                            f"average points:** "
                            f"{prediction['team_average']}"
                        )

                    with a2:

                        st.write(
                            f"**{opponent_name} "
                            f"average points:** "
                            f"{prediction['opponent_average']}"
                        )

                    st.info(
                        prediction["message"]
                    )

            else:

                st.info(
                    "Load recent match data before "
                    "running a prediction."
                )

            # =================================================
            # AI PREVIEW
            # =================================================

            st.divider()

            st.subheader(
                "🤖 AI Match Preview"
            )

            saved_summary = storage.get_summary(
                first_match.match_id
            )

            if saved_summary:

                st.success(
                    "A saved AI preview exists for "
                    "this fixture."
                )

                with st.expander(
                    "📄 View Saved AI Preview",
                    expanded=True
                ):

                    st.markdown(
                        saved_summary
                    )

                ai_col1, ai_col2 = st.columns(2)

                with ai_col1:

                    regenerate = st.button(
                        "🔄 Generate New Preview",
                        key="regenerate_preview"
                    )

                with ai_col2:

                    delete_summary = st.button(
                        "🗑️ Delete Saved Preview",
                        key="delete_preview"
                    )

                if delete_summary:

                    try:

                        storage.delete_summary(
                            first_match.match_id
                        )

                        st.success(
                            "Saved preview deleted."
                        )

                        st.rerun()

                    except StorageError as error:

                        show_error(error)

            else:

                regenerate = st.button(
                    "✨ Generate AI Preview",
                    key="generate_preview"
                )

            if gemini is None:

                st.warning(
                    "Gemini is currently unavailable. "
                    "Check your API configuration."
                )

            elif regenerate:

                try:

                    with st.spinner(
                        "Gemini is preparing the preview..."
                    ):

                        opponent_team = (
                            find_opponent_team(
                                opponent_name
                            )
                        )

                        opponent_matches = (
                            api_client.get_last_events(
                                opponent_team.team_id
                            )
                        )

                        opponent_analyzer = (
                            MatchAnalyzer(
                                opponent_team.name
                            )
                        )

                        opponent_form = (
                            opponent_analyzer.form_string(
                                opponent_matches
                            )
                        )

                        if (
                            first_match.home_team.lower()
                            == selected_team.name.lower()
                        ):

                            home_form = form

                            away_form = opponent_form

                        else:

                            home_form = opponent_form

                            away_form = form

                        preview = (
                            gemini.generate_preview(
                                home_team=first_match.home_team,
                                away_team=first_match.away_team,
                                home_form=home_form,
                                away_form=away_form,
                                fixture_date=first_match.date,
                                venue=first_match.venue
                            )
                        )

                    st.markdown(
                        preview
                    )

                    storage.save_summary(
                        first_match.match_id,
                        preview
                    )

                    st.success(
                        "AI preview generated and saved."
                    )

                except (
                    SportsAPIError,
                    GeminiAPIError,
                    StorageError
                ) as error:

                    show_error(error)

        else:

            st.divider()

            st.info(
                "No upcoming fixtures available."
            )


# =========================================================
# FAVOURITES PAGE
# =========================================================

elif page == "⭐ Favourites":

    st.header(
        "⭐ Favourite Teams"
    )

    favourites = (
        storage.get_favourite_teams()
    )

    if not favourites:

        st.info(
            "You haven't added any favourite teams yet."
        )

    else:

        st.write(
            f"You have **{len(favourites)}** "
            "favourite team(s)."
        )

        for team in favourites:

            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [3, 2, 1]
                )

                with col1:

                    st.subheader(
                        team["name"]
                    )

                    st.write(
                        f"{team['league']} • "
                        f"{team['country']}"
                    )

                with col2:

                    st.write(
                        f"Sport: {team['sport']}"
                    )

                with col3:

                    if st.button(
                        "Remove",
                        key=f"remove_{team['team_id']}"
                    ):

                        try:

                            storage.remove_favourite_team(
                                team["team_id"]
                            )

                            st.success(
                                "Removed from favourites."
                            )

                            st.rerun()

                        except StorageError as error:

                            show_error(error)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Sports Match Analyzer • Python Advanced Project"
)