
import streamlit as st
import pandas as pd
import random
import time
import os
import cv2
import numpy as np
from PIL import Image
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ================= PAGE SETTINGS =================

st.set_page_config(
    page_title="AI Music Recommender",
    page_icon="🎵",
    layout="wide"
)

# ================= DATASET =================

csv_path = os.path.join(os.path.dirname(__file__), "songs.csv")
df = pd.read_csv(csv_path)

# ================= AI ENGINE =================

df["combined_features"] = (
    df["artist"] + " " +
    df["genre"] + " " +
    df["mood"]
)

vectorizer = CountVectorizer()
feature_vectors = vectorizer.fit_transform(df["combined_features"])

similarity = cosine_similarity(feature_vectors)

# ================= CUSTOM CSS =================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg, #0f1419, #1a1f2e);
    color:white;
}

.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#00d4ff;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#b0b0b0;
    margin-bottom:30px;
}

.song-card{
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 150, 150, 0.1));
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    border-left: 4px solid #00d4ff;
}

.song-title{
    font-size:28px;
    font-weight:bold;
    color:#00d4ff;
}

.song-artist{
    color:#a0d4ff;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================

def get_song_recommendations(song_name):

    matching = df[
        df['song'].str.lower().str.contains(song_name.lower(), na=False)
    ]

    if matching.empty:
        return pd.DataFrame()

    song_index = matching.index[0]

    similarity_scores = list(enumerate(similarity[song_index]))

    sorted_songs = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_indices = [
        i[0] for i in sorted_songs[1:11]
    ]

    recommendations = df.iloc[recommended_indices]

    return recommendations


def detect_mood_from_image(image: Image.Image) -> str | None:
    """Detects a simple mood from a camera image using smile detection."""
    try:
        img = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.7,
                minNeighbors=22,
                minSize=(25, 25)
            )
            if len(smiles) > 0:
                return "Happy"

        if len(faces) > 0:
            return "Chill"

    except Exception:
        return None

    return None


# ================= HEADER =================

st.markdown(
    '<div class="main-title">🎵 AI Music Recommender Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Music Discovery Powered by AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="text-align:center; margin-bottom:20px;">'
    '<a href="http://localhost:8501" target="_blank" style="color:#00d4ff; text-decoration:none; font-weight:600;">'
    '🌐 Open Global App Link'
    '</a></div>',
    unsafe_allow_html=True
)

# ================= SEARCH =================

col1, col2 = st.columns([2, 1])

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Popularity", "Year"]
    )

with col1:
    search_song = st.text_input(
        "🔍 Search Song",
        placeholder="Type song name..."
    )

st.markdown("### Detect mood from camera")
camera_image = st.camera_input("Take a quick selfie to detect mood")
detected_mood = None

if camera_image:
    captured_image = Image.open(camera_image)
    detected_mood = detect_mood_from_image(captured_image)
    if detected_mood:
        st.success(f"Detected mood: {detected_mood}")
        st.info("If you do not enter a song, recommendations will use your detected mood.")
    else:
        st.warning("Unable to detect mood clearly. You can still search for a song manually.")

# ================= BUTTON =================

if st.button("🎧 Get AI Recommendations", use_container_width=True):

    with st.spinner("🤖 AI is finding similar songs..."):
        time.sleep(1)

        if search_song.strip() == "":
            if detected_mood:
                recommendations = df[df['mood'] == detected_mood]
                if recommendations.empty:
                    recommendations = df.sort_values(
                        "popularity",
                        ascending=False
                    ).head(10)
            else:
                recommendations = df.sort_values(
                    "popularity",
                    ascending=False
                ).head(10)

        else:
            recommendations = get_song_recommendations(search_song)
            if recommendations.empty and detected_mood:
                st.info("No exact song match found. Showing mood-based recommendations instead.")
                recommendations = df[df['mood'] == detected_mood]

    # ================= RESULTS =================

    if len(recommendations) > 0:

        st.success(f"✨ Found {len(recommendations)} recommended songs!")

        # Sorting
        if sort_by == "Popularity":
            recommendations = recommendations.sort_values(
                "popularity",
                ascending=False
            )

        if sort_by == "Year":
            recommendations = recommendations.sort_values(
                "year",
                ascending=False
            )

        # Chart
        fig = px.bar(
            recommendations,
            x="song",
            y="popularity",
            color="artist",
            title="Popularity Scores"
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Song cards
        for idx, row in recommendations.iterrows():

            st.markdown(f"""<div class="song-card"><div class="song-title">🎵 {row['song']}</div><div class="song-artist">🎤 {row['artist']}</div><br>⭐ Popularity: {row['popularity']} <br>🎸 Genre: {row['genre']} <br>📅 Year: {row['year']} <br>🎭 Mood: {row['mood']}</div>""", unsafe_allow_html=True)

            youtube_link = (
                f"https://www.youtube.com/results?search_query="
                f"{row['song']}+{row['artist']}"
            )

            spotify_link = (
                f"https://open.spotify.com/search/{row['song']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"[▶️ Listen on YouTube]({youtube_link})"
                )

            with col2:
                st.markdown(
                    f"[🎧 Open in Spotify]({spotify_link})"
                )

    else:
        st.warning("😔 No similar songs found.")

# ================= FOOTER =================

st.markdown("---")

quotes = [
    "🎵 Music is the universal language of mankind",
    "✨ Where words fail, music speaks",
    "🎧 Music gives a soul to the universe",
    "💫 Music is the soundtrack of your life"
]

st.markdown(
    f"<h3 style='text-align:center;'>"
    f"{random.choice(quotes)}"
    f"</h3>",
    unsafe_allow_html=True
)