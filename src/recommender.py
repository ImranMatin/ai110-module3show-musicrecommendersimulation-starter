import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Columns in data/songs.csv that must be read as numbers, not strings.
FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness"}
INT_FIELDS = {"id", "tempo_bpm"}

# Algorithm Recipe weights (see README "How The System Works").
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ACOUSTIC_POINTS = 0.5
ACOUSTIC_THRESHOLD = 0.5  # a song counts as "acoustic" at/above this acousticness


@dataclass
class Song:
    """A single song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences used to score songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Scores and ranks Song objects against a UserProfile (OOP interface)."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against the user, returning (score, reasons)."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += GENRE_POINTS
            reasons.append(f"genre match ({song.genre}) (+{GENRE_POINTS})")

        if song.mood == user.favorite_mood:
            score += MOOD_POINTS
            reasons.append(f"mood match ({song.mood}) (+{MOOD_POINTS})")

        # Energy closeness: 1.0 when identical, approaching 0 as it diverges.
        energy_closeness = 1.0 - abs(song.energy - user.target_energy)
        score += energy_closeness
        reasons.append(
            f"energy close to {user.target_energy} (+{energy_closeness:.2f})"
        )

        if user.likes_acoustic and song.acousticness >= ACOUSTIC_THRESHOLD:
            score += ACOUSTIC_POINTS
            reasons.append(f"acoustic pick (+{ACOUSTIC_POINTS})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Songs for the user, highest score first."""
        ranked = sorted(
            self.songs, key=lambda s: self._score(user, s)[0], reverse=True
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation for why a song was recommended."""
        _, reasons = self._score(user, song)
        return "; ".join(reasons) if reasons else "no strong match"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields parsed."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key, value in list(row.items()):
                if key in INT_FIELDS:
                    row[key] = int(value)
                elif key in FLOAT_FIELDS:
                    row[key] = float(value)
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song dict against user_prefs, returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match ({song['genre']}) (+{GENRE_POINTS})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match ({song['mood']}) (+{MOOD_POINTS})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_closeness = 1.0 - abs(song["energy"] - target_energy)
        score += energy_closeness
        reasons.append(f"energy close to {target_energy} (+{energy_closeness:.2f})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_POINTS
        reasons.append(f"acoustic pick (+{ACOUSTIC_POINTS})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank highest first, and return the top k with explanations."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
