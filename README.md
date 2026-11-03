# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders (Spotify, YouTube, Netflix) look at what you've liked
before and find new items that are *similar* along features they can measure,
then rank everything and show you the best few. They don't "understand" music —
they compare numbers and categories. My version does the same thing in miniature:
it compares each song's attributes to a user's stated taste, gives every song a
score, and returns the highest-scoring tracks. It **prioritizes genre and mood
matches first** (the strongest identity signals), then rewards songs whose
*energy* is closest to what the user wants, with a small bonus for acousticness
when the user prefers acoustic music.

**Features each `Song` uses:**

- `genre` — categorical identity (pop, lofi, rock, jazz, …)
- `mood` — categorical feel (happy, chill, intense, focused, …)
- `energy` — 0.0–1.0, how calm vs. hyped the track is
- `acousticness` — 0.0–1.0, how acoustic vs. produced it sounds
- (`valence`, `danceability`, `tempo_bpm` are available for later experiments)

**What the `UserProfile` stores:**

- `favorite_genre` — the genre to match on
- `favorite_mood` — the mood to match on
- `target_energy` — the energy level the user is aiming for (0.0–1.0)
- `likes_acoustic` — whether to reward acoustic songs

**How a score is computed (Scoring Rule, per song):**

```
score = 2.0 * (genre matches)
      + 1.0 * (mood matches)
      + 1.0 * (1 - |song.energy - target_energy|)   # closeness, not "bigger"
      + 0.5 * (acoustic match when likes_acoustic)
```

Genre is weighted highest because it's the strongest signal of taste; energy is
scored by *closeness* so a user who wants low energy isn't shown the most intense
track.

**How songs are chosen (Ranking Rule, whole catalog):** score every song, sort
by score from highest to lowest, and return the top `k`. Each recommendation also
carries a short explanation of *why* it scored well.

### Example User Profile

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
}
```

### Data Flow

```
   INPUT                    PROCESS (the loop)                 OUTPUT
┌───────────┐        ┌──────────────────────────┐        ┌──────────────┐
│ user_prefs│  ───▶  │ for each song in catalog: │  ───▶  │ sort by score│
│  (profile)│        │   score_song(prefs, song) │        │ take top K   │
│           │        │   → (score, reasons)      │        │ → ranked list│
│ songs.csv │  ───▶  │                           │        │ + why        │
└───────────┘        └──────────────────────────┘        └──────────────┘
```

A single song travels: **CSV row → scored against the profile → placed in the
ranked list**. `score_song` judges one song; `recommend_songs` loops, sorts, and
returns the top K.

### Finalized Algorithm Recipe

| Rule | Points |
|------|--------|
| Genre matches `favorite_genre` | **+2.0** |
| Mood matches `favorite_mood` | **+1.0** |
| Energy closeness to `target_energy` | **+ (1 − \|song.energy − target_energy\|)** |
| Song is acoustic AND user `likes_acoustic` | **+0.5** |

### Potential Biases

- **Genre over-prioritization.** Because genre is weighted highest (+2.0), the
  system may bury a song that perfectly matches the user's mood and energy just
  because its genre label differs — e.g., a chill, low-energy *jazz* track could
  lose to a mediocre *lofi* track for a lofi fan.
- **Popularity of common labels.** Genres/moods that appear more often in the
  catalog get more chances to match, so rare genres are structurally
  disadvantaged.
- **Ignored dimensions.** `valence`, `tempo_bpm`, and `danceability` don't affect
  the score, so two songs that feel very different (happy vs. sad) can tie.
- **Hard categorical matching.** Genre/mood are all-or-nothing; "indie pop" earns
  nothing for a "pop" fan even though they're close neighbors.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is real output from `python -m src.main` for the default pop / happy /
high-energy profile:

```
Loaded songs: 18

User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

Top recommendations:

1. Sunrise City — Neon Echo  (score: 3.98)
   reasons: genre match (pop) (+2.0); mood match (happy) (+1.0); energy close to 0.8 (+0.98)

2. Gym Hero — Max Pulse  (score: 2.87)
   reasons: genre match (pop) (+2.0); energy close to 0.8 (+0.87)

3. Rooftop Lights — Indigo Parade  (score: 1.96)
   reasons: mood match (happy) (+1.0); energy close to 0.8 (+0.96)

4. Concrete Jungle — MC Vantage  (score: 0.98)
   reasons: energy close to 0.8 (+0.98)

5. Night Drive Loop — Neon Echo  (score: 0.95)
   reasons: energy close to 0.8 (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Stress test across diverse profiles

I ran five profiles through the recommender, including two "adversarial" profiles
with conflicting preferences, via `python -m src.main`:

```
=== Profile: High-Energy Pop ===
preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}

1. Sunrise City — Neon Echo  (score: 3.92)
   reasons: genre match (pop) (+2.0); mood match (happy) (+1.0); energy close to 0.9 (+0.92)
2. Gym Hero — Max Pulse  (score: 2.97)
   reasons: genre match (pop) (+2.0); energy close to 0.9 (+0.97)
3. Rooftop Lights — Indigo Parade  (score: 1.86)
   reasons: mood match (happy) (+1.0); energy close to 0.9 (+0.86)
4. Storm Runner — Voltline  (score: 0.99)
   reasons: energy close to 0.9 (+0.99)
5. Pulse Reactor — Hz Division  (score: 0.95)
   reasons: energy close to 0.9 (+0.95)

=== Profile: Chill Lofi ===
preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}

1. Library Rain — Paper Lanterns  (score: 4.50)
   reasons: genre match (lofi) (+2.0); mood match (chill) (+1.0); energy close to 0.35 (+1.00); acoustic pick (+0.5)
2. Midnight Coding — LoRoom  (score: 4.43)
   reasons: genre match (lofi) (+2.0); mood match (chill) (+1.0); energy close to 0.35 (+0.93); acoustic pick (+0.5)
3. Focus Flow — LoRoom  (score: 3.45)
   reasons: genre match (lofi) (+2.0); energy close to 0.35 (+0.95); acoustic pick (+0.5)
4. Spacewalk Thoughts — Orbit Bloom  (score: 2.43)
   reasons: mood match (chill) (+1.0); energy close to 0.35 (+0.93); acoustic pick (+0.5)
5. Coffee Shop Stories — Slow Stereo  (score: 1.48)
   reasons: energy close to 0.35 (+0.98); acoustic pick (+0.5)

=== Profile: Deep Intense Rock ===
preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}

1. Storm Runner — Voltline  (score: 3.99)
   reasons: genre match (rock) (+2.0); mood match (intense) (+1.0); energy close to 0.9 (+0.99)
2. Gym Hero — Max Pulse  (score: 1.97)
   reasons: mood match (intense) (+1.0); energy close to 0.9 (+0.97)
3. Pulse Reactor — Hz Division  (score: 0.95)
   reasons: energy close to 0.9 (+0.95)
4. Iron Veins — Blackforge  (score: 0.93)
   reasons: energy close to 0.9 (+0.93)
5. Sunrise City — Neon Echo  (score: 0.92)
   reasons: energy close to 0.9 (+0.92)

=== Profile: Conflicting (ambient + aggressive + high energy) ===
preferences: {'genre': 'ambient', 'mood': 'aggressive', 'energy': 0.95}

1. Spacewalk Thoughts — Orbit Bloom  (score: 2.33)
   reasons: genre match (ambient) (+2.0); energy close to 0.95 (+0.33)
2. Iron Veins — Blackforge  (score: 1.98)
   reasons: mood match (aggressive) (+1.0); energy close to 0.95 (+0.98)
3. Pulse Reactor — Hz Division  (score: 1.00)
   reasons: energy close to 0.95 (+1.00)
4. Gym Hero — Max Pulse  (score: 0.98)
   reasons: energy close to 0.95 (+0.98)
5. Storm Runner — Voltline  (score: 0.96)
   reasons: energy close to 0.95 (+0.96)

=== Profile: Conflicting (high energy + melancholy) ===
preferences: {'genre': 'classical', 'mood': 'melancholy', 'energy': 0.9}

1. Moonlit Sonata Redux — Clara Vey  (score: 3.40)
   reasons: genre match (classical) (+2.0); mood match (melancholy) (+1.0); energy close to 0.9 (+0.40)
2. Storm Runner — Voltline  (score: 0.99)
   reasons: energy close to 0.9 (+0.99)
3. Gym Hero — Max Pulse  (score: 0.97)
   reasons: energy close to 0.9 (+0.97)
4. Pulse Reactor — Hz Division  (score: 0.95)
   reasons: energy close to 0.9 (+0.95)
5. Iron Veins — Blackforge  (score: 0.93)
   reasons: energy close to 0.9 (+0.93)
```

### Weight-shift experiment (genre 2.0 → 1.0, energy ×2)

For the High-Energy Pop profile, halving the genre weight and doubling the energy
weight produced the **same top-5 order**, only with compressed scores (Rooftop
Lights narrowed the gap on Gym Hero). The ranking barely moved because this
catalog's pop songs also happen to be high-energy, so genre and energy reinforce
each other instead of competing. Takeaway: the change made the results *different*,
not clearly *more accurate* — a sign the dataset is too small and correlated to
really exercise the weights.

Other experiment ideas for later:

- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



