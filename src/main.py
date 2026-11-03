"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Named taste profiles used to stress-test the recommender, including two
# "adversarial" profiles with conflicting preferences.
PROFILES = {
    "High-Energy Pop (modern hits, no explicit)": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "favorite_decade": 2020,
        "prefers_popular": True,
        "desired_mood_tags": ["euphoric", "upbeat"],
        "avoid_explicit": True,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    # Adversarial: wants a calm genre but cranked-up energy + an angry mood.
    "Conflicting (ambient + aggressive + high energy)": {
        "genre": "ambient",
        "mood": "aggressive",
        "energy": 0.95,
    },
    # Adversarial: high energy but a sad mood (energy/mood pull apart).
    "Conflicting (high energy + melancholy)": {
        "genre": "classical",
        "mood": "melancholy",
        "energy": 0.9,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(f"\n=== Profile: {name} ===")
        print(f"preferences: {user_prefs}\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
            print(f"   reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()
