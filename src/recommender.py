import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# Columns in data/songs.csv that must be read as numbers, not strings.
FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness", "instrumentalness"}
INT_FIELDS = {"id", "tempo_bpm", "popularity", "release_decade"}
BOOL_FIELDS = {"explicit"}

# Algorithm Recipe weights (see README "How The System Works").
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ACOUSTIC_POINTS = 0.5
ACOUSTIC_THRESHOLD = 0.5  # a song counts as "acoustic" at/above this acousticness

# Advanced-feature weights (Challenge 1).
DECADE_POINTS = 1.0            # exact release-decade match
POPULARITY_WEIGHT = 1.0        # scaled by popularity/100 when the user wants hits
MOOD_TAG_POINTS = 0.5          # per overlapping detailed mood tag
MOOD_TAG_CAP = 1.5             # most the mood-tag overlap can contribute
INSTRUMENTAL_POINTS = 0.5      # bonus for instrumental tracks when preferred
INSTRUMENTAL_THRESHOLD = 0.5
EXPLICIT_PENALTY = 1.0         # subtracted for explicit songs when the user avoids them


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
    # Advanced features (defaults keep older callers and tests working).
    popularity: int = 0
    release_decade: int = 0
    mood_tags: List[str] = field(default_factory=list)
    instrumentalness: float = 0.0
    explicit: bool = False


@dataclass
class UserProfile:
    """A user's taste preferences used to score songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Advanced preferences (all optional; omitting them keeps baseline scoring).
    favorite_decade: Optional[int] = None
    prefers_popular: bool = False
    desired_mood_tags: List[str] = field(default_factory=list)
    likes_instrumental: bool = False
    avoid_explicit: bool = False


def _advanced_points(
    song_popularity: int,
    song_decade: int,
    song_tags: List[str],
    song_instrumentalness: float,
    song_explicit: bool,
    favorite_decade: Optional[int],
    prefers_popular: bool,
    desired_tags: List[str],
    likes_instrumental: bool,
    avoid_explicit: bool,
) -> Tuple[float, List[str]]:
    """Score the advanced features shared by both the dict and Song paths."""
    score = 0.0
    reasons: List[str] = []

    if favorite_decade is not None and song_decade == favorite_decade:
        score += DECADE_POINTS
        reasons.append(f"from favorite decade ({song_decade}s) (+{DECADE_POINTS})")

    if prefers_popular and song_popularity:
        pop_bonus = POPULARITY_WEIGHT * (song_popularity / 100.0)
        score += pop_bonus
        reasons.append(f"popular ({song_popularity}/100) (+{pop_bonus:.2f})")

    if desired_tags and song_tags:
        shared = [t for t in song_tags if t in desired_tags]
        if shared:
            tag_bonus = min(MOOD_TAG_POINTS * len(shared), MOOD_TAG_CAP)
            score += tag_bonus
            reasons.append(f"mood tags {shared} (+{tag_bonus:.2f})")

    if likes_instrumental and song_instrumentalness >= INSTRUMENTAL_THRESHOLD:
        score += INSTRUMENTAL_POINTS
        reasons.append(f"instrumental (+{INSTRUMENTAL_POINTS})")

    if avoid_explicit and song_explicit:
        score -= EXPLICIT_PENALTY
        reasons.append(f"explicit content (-{EXPLICIT_PENALTY})")

    return score, reasons


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

        adv_score, adv_reasons = _advanced_points(
            song.popularity,
            song.release_decade,
            song.mood_tags,
            song.instrumentalness,
            song.explicit,
            user.favorite_decade,
            user.prefers_popular,
            user.desired_mood_tags,
            user.likes_instrumental,
            user.avoid_explicit,
        )
        score += adv_score
        reasons.extend(adv_reasons)

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
                elif key in BOOL_FIELDS:
                    row[key] = value.strip().lower() == "true"
                elif key == "mood_tags":
                    row[key] = [t for t in value.split("|") if t]
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

    adv_score, adv_reasons = _advanced_points(
        song.get("popularity", 0),
        song.get("release_decade", 0),
        song.get("mood_tags", []),
        song.get("instrumentalness", 0.0),
        song.get("explicit", False),
        user_prefs.get("favorite_decade"),
        user_prefs.get("prefers_popular", False),
        user_prefs.get("desired_mood_tags", []),
        user_prefs.get("likes_instrumental", False),
        user_prefs.get("avoid_explicit", False),
    )
    score += adv_score
    reasons.extend(adv_reasons)

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
