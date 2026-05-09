import streamlit as st
import random

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Music Recommender",
    page_icon="🎵",
    layout="centered"
)

# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #020617);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

.song-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 15px;
    margin-top: 15px;
    border-left: 5px solid #38bdf8;
    box-shadow: 0px 0px 12px rgba(56,189,248,0.2);
}

.quote-box {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
    text-align: center;
    color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)

# SONG DATA
songs = {

    "Happy": [
        ("Happy - Pharrell Williams",
         "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),

        ("Uptown Funk - Bruno Mars",
         "https://www.youtube.com/watch?v=OPf0YbXqDm0"),

        ("Can't Stop The Feeling",
         "https://www.youtube.com/watch?v=ru0K8uYEZWw")
    ],

    "Sad": [
        ("Someone Like You - Adele",
         "https://www.youtube.com/watch?v=hLQl3WQQoQ0"),

        ("Fix You - Coldplay",
         "https://www.youtube.com/watch?v=k4V3Mo61fJM"),

        ("Let Her Go - Passenger",
         "https://www.youtube.com/watch?v=RBumgq5yVrA")
    ],

    "Relaxed": [
        ("Perfect - Ed Sheeran",
         "https://www.youtube.com/watch?v=2Vv-BfVoq4g"),

        ("Photograph - Ed Sheeran",
         "https://www.youtube.com/watch?v=nSDgHBxUbVQ"),

        ("Memories - Maroon 5",
         "https://www.youtube.com/watch?v=SlPhMPnQ58k")
    ],

    "Energetic": [
        ("Believer - Imagine Dragons",
         "https://www.youtube.com/watch?v=7wtfhZwyrcc"),

        ("Thunder - Imagine Dragons",
         "https://www.youtube.com/watch?v=fKopy74weus"),

        ("Hall Of Fame - The Script",
         "https://www.youtube.com/watch?v=mk48xRzuNvA")
    ]
}

# MOTIVATION QUOTES
quotes = [
    "Music is the strongest form of magic ✨",
    "Feel the music, live the moment 🎶",
    "Good music heals everything ❤️",
    "Your mood decides your playlist 🎧"
]

# TITLE
st.markdown(
    '<div class="main-title">🎵 AI Music Recommender</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Get songs based on your mood</div>',
    unsafe_allow_html=True
)

# FEATURE 1 → Mood Selection
mood = st.selectbox(
    "Choose Your Mood",
    ["Happy", "Sad", "Relaxed", "Energetic"]
)

# FEATURE 2 → Music Type
music_type = st.radio(
    "Choose Music Type",
    ["English", "Chill", "Party"]
)

# BUTTON
if st.button("🎶 Recommend Songs"):

    st.success(f"Showing {mood} songs")

    for song, link in songs[mood]:

        st.markdown(
            f"""
            <div class="song-box">
                <h3>{song}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "▶ Listen on YouTube",
            link
        )

    # RANDOM QUOTE FEATURE
    st.markdown(
        f"""
        <div class="quote-box">
            {random.choice(quotes)}
        </div>
        """,
        unsafe_allow_html=True
    )

# SIDEBAR
st.sidebar.title("🎧 About")

st.sidebar.info("""
This AI Music Recommender suggests songs based on your mood.

Features:
✅ Mood-based recommendations  
✅ YouTube song links  
✅ Music categories  
✅ Motivational quotes  
""")