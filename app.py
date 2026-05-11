import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import cv2
import numpy as np
from PIL import Image
import textwrap

# ================= PAGE SETTINGS =================

st.set_page_config(
    page_title="AI Music Recommender",
    page_icon="🎵",
    layout="wide"
)

# ================= DATASET =================

data = {
    "song": [
        "Happy", "Uptown Funk", "Can't Stop The Feeling", "Shape of You",
        "Someone Like You", "Fix You", "Let Her Go", "Photograph",
        "Perfect", "Memories", "Faded", "Closer", "Believer",
        "Thunder", "Hall Of Fame", "Stronger", "Blinding Lights",
        "Levitating", "Animals", "Titanium", "Dance Monkey", "Circles",
        "Watermelon Sugar", "Bad Guy", "Old Town Road"
    ],

    "artist": [
        "Pharrell Williams", "Bruno Mars", "Justin Timberlake", "Ed Sheeran",
        "Adele", "Coldplay", "Passenger", "Ed Sheeran", "Ed Sheeran",
        "Maroon 5", "Alan Walker", "Chainsmokers", "Imagine Dragons",
        "Imagine Dragons", "The Script", "Kanye West", "The Weeknd",
        "Dua Lipa", "Martin Garrix", "David Guetta", "Tones And I",
        "Post Malone", "Harry Styles", "Billie Eilish", "Lil Nas X"
    ],

    "genre": [
        "Pop", "Funk", "Pop", "Pop", "Ballad", "Alternative", "Folk",
        "Pop", "Pop", "Pop", "Electronic", "Electronic", "Rock",
        "Rock", "Pop", "Hip Hop", "R&B", "Disco", "Electronic",
        "Electronic", "Pop", "R&B", "Pop", "Pop", "Country"
    ],

    "mood": [
        "Happy", "Happy", "Happy", "Happy", "Sad", "Sad", "Sad",
        "Sad", "Romantic", "Nostalgic", "Chill", "Chill",
        "Energetic", "Energetic", "Inspirational", "Energetic",
        "Party", "Party", "Party", "Party", "Dance", "Chill",
        "Happy", "Dark", "Country"
    ],

    "year": [
        2013, 2014, 2016, 2017, 2011, 2005, 2012, 2014, 2017,
        2019, 2015, 2016, 2017, 2017, 2012, 2007, 2019, 2020,
        2013, 2011, 2019, 2019, 2019, 2019, 2019
    ],

    "popularity": [
        95, 98, 92, 99, 94, 93, 91, 90, 96, 88, 89, 93, 97,
        94, 92, 88, 99, 96, 87, 91, 95, 91, 98, 94, 97
    ]
}

df = pd.DataFrame(data)

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

st.markdown(textwrap.dedent("""
<style>

.stApp{
    background: linear-gradient(135deg,#667eea,#764ba2);
    color:white;
}

.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#dddddd;
    margin-bottom:30px;
}

.song-card{
    background: rgba(255,255,255,0.1);
    padding:20px;
    border-radius:20px;
    margin-bottom:15px;
}

.song-title{
    font-size:28px;
    font-weight:bold;
    color:white;
}

.song-artist{
    color:#eeeeee;
    font-size:18px;
}

</style>
"""), unsafe_allow_html=True)

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

def detect_mood_from_image(image):
    # Convert PIL Image to OpenCV format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    
    # Load Haar cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return "Chill"  # Default mood if no face detected
    
    # Check for smiles in detected faces
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))
        
        if len(smiles) > 0:
            return "Happy"
    
    return "Chill"

def get_mood_recommendations(mood):
    mood_songs = df[df['mood'].str.lower() == mood.lower()]
    if mood_songs.empty:
        return df.head(10)  # Fallback to top songs
    return mood_songs.head(10)


# ================= HEADER =================

st.markdown(
    '<div class="main-title">🎵 AI Music Recommender Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Music Discovery Powered by AI</div>',
    unsafe_allow_html=True
)

# ================= SEARCH =================

col1, col2 = st.columns([3,1])

with col1:
    search_song = st.text_input(
        "🔍 Search Song",
        placeholder="Type song name..."
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Popularity", "Year"]
    )

# ================= CAMERA MOOD DETECTION =================

st.markdown("### 📸 Detect Mood from Camera")

camera_image = st.camera_input("Take a photo to detect your mood")

detected_mood = None

if camera_image is not None:
    image = Image.open(camera_image)
    detected_mood = detect_mood_from_image(image)
    st.success(f"🎭 Detected Mood: {detected_mood}")

# ================= BUTTON =================

if st.button("🎧 Get AI Recommendations", use_container_width=True):

    with st.spinner("🤖 AI is finding similar songs..."):
        time.sleep(1)

        if detected_mood is not None:
            recommendations = get_mood_recommendations(detected_mood)
        elif search_song.strip() == "":
            recommendations = df.sort_values(
                "popularity",
                ascending=False
            ).head(10)
        else:
            recommendations = get_song_recommendations(search_song)

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

            st.markdown(
                f"""
**🎵 {row['song']}**  
🎤 *{row['artist']}*  

⭐ **Popularity:** {row['popularity']}  
🎸 **Genre:** {row['genre']}  
📅 **Year:** {row['year']}  
🎭 **Mood:** {row['mood']}
"""
            )

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
