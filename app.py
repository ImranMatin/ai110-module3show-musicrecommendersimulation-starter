"""Streamlit web UI for the Music Recommender Simulation (runs on localhost)."""
import streamlit as st

from src.recommender import load_songs, recommend_songs

st.set_page_config(page_title="VibeFinder 1.0", page_icon="🎵")

songs = load_songs("data/songs.csv")
genres = sorted({s["genre"] for s in songs})
moods = sorted({s["mood"] for s in songs})

st.title("🎵 VibeFinder 1.0")
st.caption("A tiny content-based music recommender. Pick your vibe and get ranked songs.")

with st.sidebar:
    st.header("Your taste profile")
    genre = st.selectbox("Favorite genre", genres, index=genres.index("pop"))
    mood = st.selectbox("Favorite mood", moods, index=moods.index("happy"))
    energy = st.slider("Target energy", 0.0, 1.0, 0.8, 0.05)
    likes_acoustic = st.checkbox("I like acoustic music", value=False)
    k = st.slider("How many recommendations", 1, 10, 5)

user_prefs = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "likes_acoustic": likes_acoustic,
}

st.subheader("Top recommendations")
st.write(f"Profile: `{user_prefs}`")

for rank, (song, score, explanation) in enumerate(
    recommend_songs(user_prefs, songs, k=k), start=1
):
    with st.container(border=True):
        st.markdown(f"**{rank}. {song['title']}** — {song['artist']}")
        st.markdown(f"Score: **{score:.2f}**")
        st.caption(f"Why: {explanation}")
