# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1 — add 5+ advanced song attributes to the dataset and make the
recommender score them. The new attributes: `popularity` (0–100), `release_decade`,
`mood_tags` (detailed pipe-separated tags like `euphoric|upbeat`), `instrumentalness`
(0.0–1.0), and `explicit` (True/False).

**Prompts used:**

- "Examine data/songs.csv and src/recommender.py. Add 5 new attributes — popularity
  (0-100), release_decade, detailed mood_tags, instrumentalness, and explicit — to
  all 18 rows with realistic values, then update the scoring logic to account for
  them. Keep the existing tests passing."
- "Make sure the new Song and UserProfile fields have defaults so the existing test
  constructors (which only pass the original fields) still work."
- "Add an example profile to main.py that uses the new preferences (favorite decade,
  prefers popular, desired mood tags, avoid explicit) so I can see the new scoring
  in the output."

**What did the agent generate or change?**

- `data/songs.csv` — added 5 new columns and filled them for all 18 songs.
- `src/recommender.py` — added the new fields to the `Song` and `UserProfile`
  dataclasses (with defaults), extended `load_songs` to parse the new types
  (int/float/bool, and split `mood_tags` on `|`), and added a shared
  `_advanced_points()` helper used by both `score_song()` (dict path) and the OOP
  `Recommender._score()` (Song path). New scoring rules: +1.0 for a decade match,
  popularity×1.0 scaled by /100 when the user wants hits, +0.5 per overlapping mood
  tag (capped at +1.5), +0.5 for instrumental tracks when preferred, and a −1.0
  penalty for explicit songs when the user avoids them.
- `src/main.py` — enriched the first profile to use the new preferences.

**What did you verify or fix manually?**

- Ran `pytest` — confirmed both existing tests still pass (the dataclass defaults
  were essential; without them the test constructors would break).
- Ran `python -m src.main` and read the reasons line for the enriched profile to
  confirm each new rule fired correctly: *Sunrise City* gained the decade,
  popularity, and mood-tag bonuses; *Gym Hero* correctly took the −1.0 explicit
  penalty (it is tagged explicit). The arithmetic in the score matched the sum of
  the listed reasons.
- Checked that `load_songs` converts `explicit` to a real boolean (not the string
  "False", which would always be truthy) and that `mood_tags` becomes a list, not a
  raw pipe string.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
