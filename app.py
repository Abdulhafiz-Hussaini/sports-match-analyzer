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
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM UI STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main application spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    /* Dashboard cards */
    .dashboard-card {
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 1rem;
    }

    .team-name {
        font-size: 1.35rem;
        font-weight: 700;
    }

    .small-label {
        font-size: 0.82rem;
        opacity: 0.65;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Form badges */
    .form-badge {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        margin-right: 0.3rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        border: 1px solid rgba(128, 128, 128, 0.25);
    }

    /* Hero section */
    .hero {
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 1.5rem;
    }

    /* AI section */
    .ai-box {
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        opacity: 0.6;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
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

if "team_matches" not in st.session_state:
    st.session_state.team_matches = []

if "upcoming_matches" not in st.session_state:
    st.session_state.upcoming_matches = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "last_search" not in st.session_state:
    st.session_state.last_search = ""


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">⚽ Sports Match Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Search football teams, explore fixtures, analyse recent form,
        save favourites and generate AI-powered match insights.
    </div>
    """,
    unsafe_allow_html=True
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

    st.subheader("About")

    st.caption(
        "Sports Match Analyzer combines live football data, "
        "form analysis, local storage and AI-generated insights."
    )

    st.divider()

    st.caption("⚽ Sports data: TheSportsDB")
    st.caption("🤖 AI insights: Gemini")
    st.caption("🐍 Built with Python + Streamlit")


# =========================================================
# TEAM SEARCH PAGE
# =========================================================

if page == "🔎 Team Search":

    # =====================================================
    # SEARCH SECTION
    # =====================================================

    st.header("🔎 Find a Football Team")

    st.write(
        "Search for a team to view its information, recent results "
        "and upcoming fixtures."
    )

    search_col, button_col, clear_col = st.columns(
        [5, 1, 1]
    )

    with search_col:

        team_name = st.text_input(
            "Team name",
            placeholder="e.g. Arsenal, Barcelona, Real Madrid",
            label_visibility="collapsed"
        )

    with button_col:

        search_button = st.button(
            "🔍 Search",
            type="primary",
            use_container_width=True
        )

    with clear_col:

        clear_button = st.button(
            "Clear",
            use_container_width=True
        )

    if clear_button:

        st.session_state.search_results = []
        st.session_state.selected_team = None
        st.session_state.team_matches = []
        st.session_state.upcoming_matches = []
        st.session_state.last_search = ""

        st.rerun()

    # =====================================================
    # SEARCH ACTION
    # =====================================================

    if search_button:

        try:

            validated_name = (
                InputValidator.validate_team_name(
                    team_name
                )
            )

            with st.spinner(
                "🔎 Searching the sports database..."
            ):

                teams = api_client.search_team(
                    validated_name
                )

            st.session_state.search_results = teams
            st.session_state.last_search = validated_name
            st.session_state.selected_team = None
            st.session_state.team_matches = []
            st.session_state.upcoming_matches = []

            if teams:

                st.success(
                    f"Found {len(teams)} team(s) matching "
                    f"**{validated_name}**."
                )

        except (
            ValidationError,
            SportsAPIError
        ) as error:

            ErrorHandler.log_error(error)

            st.error(
                ErrorHandler.get_message(error)
            )

    # =====================================================
    # SEARCH RESULTS
    # =====================================================

    teams = st.session_state.search_results

    if teams:

        st.subheader("📋 Search Results")

        st.caption(
            f"Showing results for "
            f"**{st.session_state.last_search}**"
        )

        for team in teams:

            with st.container(border=True):

                result_col1, result_col2 = st.columns(
                    [5, 1]
                )

                with result_col1:

                    badge_col, details_col = st.columns(
                        [1, 5]
                    )

                    with badge_col:

                        if team.badge_url:

                            try:

                                st.image(
                                    team.badge_url,
                                    width=80
                                )

                            except Exception:

                                st.write("⚽")

                        else:

                            st.write("⚽")

                    with details_col:

                        st.markdown(
                            f'<div class="team-name">'
                            f'{team.name}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        st.write(
                            f"🏆 **League:** {team.league}"
                        )

                        st.write(
                            f"🌍 **Country:** {team.country}"
                        )

                        st.caption(
                            f"Sport: {team.sport}"
                        )

                with result_col2:

                    st.write("")

                    if st.button(
                        "View Team",
                        key=f"view_{team.team_id}",
                        use_container_width=True
                    ):

                        st.session_state.selected_team = team
                        st.session_state.team_matches = []
                        st.session_state.upcoming_matches = []

                        st.rerun()

    elif st.session_state.last_search:

        st.info(
            "No teams are currently displayed for this search."
        )


    # =====================================================
    # SELECTED TEAM
    # =====================================================

    selected_team = st.session_state.selected_team

    if selected_team:

        st.divider()

        # =================================================
        # TEAM HERO
        # =================================================

        with st.container(border=True):

            hero_col1, hero_col2 = st.columns(
                [1, 5]
            )

            with hero_col1:

                if selected_team.badge_url:

                    try:

                        st.image(
                            selected_team.badge_url,
                            width=120
                        )

                    except Exception:

                        st.markdown("## ⚽")

                else:

                    st.markdown("## ⚽")

            with hero_col2:

                st.markdown(
                    f"# {selected_team.name}"
                )

                st.caption(
                    "Selected team"
                )

                st.write(
                    f"🏆 {selected_team.league}  •  "
                    f"🌍 {selected_team.country}"
                )

        # =================================================
        # TEAM INFORMATION
        # =================================================

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
        # FAVOURITE ACTION
        # =================================================

        st.subheader("⭐ Favourite")

        try:

            favourite_status = storage.is_favourite(
                selected_team.team_id
            )

        except StorageError as error:

            ErrorHandler.log_error(error)

            favourite_status = False

            st.error(
                ErrorHandler.get_message(error)
            )

        if favourite_status:

            st.success(
                "⭐ This team is already in your favourites."
            )

        else:

            if st.button(
                "⭐ Add to Favourites",
                use_container_width=False
            ):

                try:

                    added = storage.add_favourite_team(
                        selected_team
                    )

                    if added:

                        st.success(
                            f"⭐ {selected_team.name} "
                            f"has been added to your favourites."
                        )

                        st.rerun()

                    else:

                        st.info(
                            "This team is already in your favourites."
                        )

                except StorageError as error:

                    ErrorHandler.log_error(error)

                    st.error(
                        ErrorHandler.get_message(error)
                    )

        # =================================================
        # LOAD MATCH DATA
        # =================================================

        st.subheader("📊 Match Analysis")

        if st.button(
            "📊 Load Match Analysis",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "📡 Loading recent results and upcoming fixtures..."
                ):

                    recent = (
                        api_client.get_last_events(
                            selected_team.team_id
                        )
                    )

                    upcoming = (
                        api_client.get_next_events(
                            selected_team.team_id
                        )
                    )

                st.session_state.team_matches = recent
                st.session_state.upcoming_matches = upcoming

                st.success(
                    "✅ Match data loaded successfully."
                )

            except SportsAPIError as error:

                ErrorHandler.log_error(error)

                st.error(
                    ErrorHandler.get_message(error)
                )

        # =================================================
        # MATCH DATA
        # =================================================

        if st.session_state.team_matches:

            recent_matches = (
                st.session_state.team_matches
            )

            upcoming_matches = (
                st.session_state.upcoming_matches
            )

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
            # FORM OVERVIEW
            # =============================================

            st.divider()

            st.subheader("📈 Recent Form")

            if form:

                form_display = "  ".join(
                    [
                        f"`{letter}`"
                        for letter in form.split()
                    ]
                )

                st.markdown(
                    f"**Current form:** {form_display}"
                )

            else:

                st.info(
                    "There is not enough completed match data "
                    "to display a form sequence."
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

            goals1, goals2 = st.columns(2)

            with goals1:

                st.metric(
                    "⚽ Goals Scored",
                    stats["goals_scored"]
                )

            with goals2:

                st.metric(
                    "🛡️ Goals Conceded",
                    stats["goals_conceded"]
                )

            # =============================================
            # RECENT RESULTS
            # =============================================

            st.divider()

            st.subheader("🕘 Recent Results")

            if recent_matches:

                for match in recent_matches[:5]:

                    result = match.result_for_team(
                        selected_team.name
                    )

                    with st.container(border=True):

                        match_col1, match_col2 = st.columns(
                            [4, 1]
                        )

                        with match_col1:

                            st.markdown(
                                f"**{match.display_name()}**"
                            )

                            st.caption(
                                f"📅 {match.date or 'Date unavailable'}"
                            )

                        with match_col2:

                            st.metric(
                                "Score",
                                match.score or "N/A"
                            )

                        if result == "Win":

                            st.success(
                                "🟢 Win"
                            )

                        elif result == "Draw":

                            st.info(
                                "🟡 Draw"
                            )

                        elif result == "Loss":

                            st.error(
                                "🔴 Loss"
                            )

                        else:

                            st.caption(
                                result
                            )

                        # ---------------------------------
                        # MATCH NOTE
                        # ---------------------------------

                        with st.expander(
                            "📝 Match Note"
                        ):

                            try:

                                existing_note = (
                                    storage.get_match_note(
                                        match.match_id
                                    )
                                )

                                note = st.text_area(
                                    "Add a private note",
                                    value=existing_note or "",
                                    placeholder=(
                                        "e.g. Strong defensive performance..."
                                    ),
                                    key=f"note_{match.match_id}",
                                    max_chars=1000
                                )

                                save_note_col, delete_note_col = (
                                    st.columns(2)
                                )

                                with save_note_col:

                                    if st.button(
                                        "💾 Save Note",
                                        key=f"save_note_{match.match_id}"
                                    ):

                                        try:

                                            validated_note = (
                                                InputValidator.validate_note(
                                                    note
                                                )
                                            )

                                            storage.save_match_note(
                                                match.match_id,
                                                validated_note
                                            )

                                            st.success(
                                                "Note saved."
                                            )

                                        except (
                                            ValidationError,
                                            StorageError
                                        ) as error:

                                            ErrorHandler.log_error(
                                                error
                                            )

                                            st.error(
                                                ErrorHandler.get_message(
                                                    error
                                                )
                                            )

                                with delete_note_col:

                                    if existing_note:

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

                                                ErrorHandler.log_error(
                                                    error
                                                )

                                                st.error(
                                                    ErrorHandler.get_message(
                                                        error
                                                    )
                                                )

                            except StorageError as error:

                                ErrorHandler.log_error(
                                    error
                                )

                                st.error(
                                    ErrorHandler.get_message(
                                        error
                                    )
                                )

            else:

                st.info(
                    "No recent results are available."
                )

            # =============================================
            # UPCOMING FIXTURES
            # =============================================

            st.divider()

            st.subheader("📅 Upcoming Fixtures")

            if upcoming_matches:

                for match in upcoming_matches[:5]:

                    with st.container(border=True):

                        st.markdown(
                            f"### ⚽ {match.display_name()}"
                        )

                        fixture_col1, fixture_col2 = (
                            st.columns(2)
                        )

                        with fixture_col1:

                            st.write(
                                f"📅 **Date:** "
                                f"{match.date or 'Unavailable'}"
                            )

                        with fixture_col2:

                            st.write(
                                f"📍 **Venue:** "
                                f"{match.venue or 'N/A'}"
                            )

                        if match.status:

                            st.caption(
                                f"Status: {match.status}"
                            )

            else:

                st.info(
                    "No upcoming fixtures are available."
                )

            # =============================================
            # AI MATCH PREVIEW
            # =============================================

            st.divider()

            st.subheader("🤖 AI Match Preview")

            if gemini is None:

                st.warning(
                    "Gemini is currently unavailable. "
                    "Check your GEMINI_API_KEY configuration."
                )

            elif upcoming_matches:

                match = upcoming_matches[0]

                if (
                    match.home_team.lower()
                    == selected_team.name.lower()
                ):

                    opponent = match.away_team

                else:

                    opponent = match.home_team

                st.write(
                    f"AI analysis for the next fixture: "
                    f"**{match.home_team} vs {match.away_team}**"
                )

                if st.button(
                    "✨ Generate AI Preview",
                    type="primary"
                ):

                    try:

                        with st.spinner(
                            "🤖 Gemini is preparing the preview..."
                        ):

                            opponent_results = (
                                api_client.search_team(
                                    opponent
                                )
                            )

                            if not opponent_results:

                                raise SportsAPIError(
                                    f"Could not find {opponent}."
                                )

                            opponent_team = (
                                opponent_results[0]
                            )

                            opponent_matches = (
                                api_client.get_last_events(
                                    opponent_team.team_id
                                )
                            )

                            selected_is_home = (
                                match.home_team.lower()
                                == selected_team.name.lower()
                            )

                            if selected_is_home:

                                home_form = form

                                away_form = (
                                    MatchAnalyzer(
                                        opponent_team.name
                                    ).form_string(
                                        opponent_matches
                                    )
                                )

                            else:

                                home_form = (
                                    MatchAnalyzer(
                                        opponent_team.name
                                    ).form_string(
                                        opponent_matches
                                    )
                                )

                                away_form = form

                            preview = (
                                gemini.generate_preview(
                                    home_team=match.home_team,
                                    away_team=match.away_team,
                                    home_form=home_form,
                                    away_form=away_form,
                                    fixture_date=match.date,
                                    venue=match.venue
                                )
                            )

                        st.markdown(
                            '<div class="ai-box">',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            preview
                        )

                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )

                        try:

                            storage.save_summary(
                                match.match_id,
                                preview
                            )

                            st.success(
                                "🤖 AI preview generated "
                                "and saved successfully."
                            )

                        except StorageError as error:

                            ErrorHandler.log_error(
                                error
                            )

                            st.warning(
                                "Preview generated, but "
                                "could not be saved."
                            )

                    except (
                        SportsAPIError,
                        GeminiAPIError,
                        StorageError
                    ) as error:

                        ErrorHandler.log_error(
                            error
                        )

                        st.error(
                            ErrorHandler.get_message(
                                error
                            )
                        )

            else:

                st.info(
                    "No upcoming fixture is available "
                    "for an AI preview."
                )

        else:

            st.info(
                "Click **Load Match Analysis** to retrieve "
                "recent results and upcoming fixtures."
            )


# =========================================================
# FAVOURITES PAGE
# =========================================================

elif page == "⭐ Favourites":

    st.header("⭐ Favourite Teams")

    st.write(
        "Your saved teams are stored locally and remain "
        "available when you reopen the application."
    )

    try:

        favourites = (
            storage.get_favourite_teams()
        )

    except StorageError as error:

        ErrorHandler.log_error(
            error
        )

        st.error(
            ErrorHandler.get_message(
                error
            )
        )

        favourites = []

    if not favourites:

        st.info(
            "⭐ You haven't added any favourite teams yet."
        )

        st.write(
            "Go to **Team Search**, select a team and "
            "click **Add to Favourites**."
        )

    else:

        st.success(
            f"You currently have "
            f"**{len(favourites)}** favourite team(s)."
        )

        for team in favourites:

            with st.container(border=True):

                fav_col1, fav_col2, fav_col3 = (
                    st.columns([1, 4, 1])
                )

                with fav_col1:

                    if team.get("badge_url"):

                        try:

                            st.image(
                                team["badge_url"],
                                width=65
                            )

                        except Exception:

                            st.markdown("⚽")

                    else:

                        st.markdown("⚽")

                with fav_col2:

                    st.subheader(
                        team["name"]
                    )

                    st.write(
                        f"🏆 {team.get('league', 'Unknown')} "
                        f"• 🌍 {team.get('country', 'Unknown')}"
                    )

                with fav_col3:

                    if st.button(
                        "Remove",
                        key=f"remove_{team['team_id']}",
                        use_container_width=True
                    ):

                        try:

                            removed = (
                                storage.remove_favourite_team(
                                    team["team_id"]
                                )
                            )

                            if removed:

                                st.success(
                                    "Removed from favourites."
                                )

                                st.rerun()

                            else:

                                st.info(
                                    "Team was not found "
                                    "in favourites."
                                )

                        except StorageError as error:

                            ErrorHandler.log_error(
                                error
                            )

                            st.error(
                                ErrorHandler.get_message(
                                    error
                                )
                            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        ⚽ <strong>Sports Match Analyzer</strong><br>
        Python Advanced Group Project • Streamlit Application
    </div>
    """,
    unsafe_allow_html=True
)