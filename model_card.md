# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Think of the model as a judge handing out points. For every song in the catalog,
it looks at three things about the listener: the genre they like, the mood they're
in, and how energetic they want the music to feel. Each song then earns points for
how well it matches:

- If the song's **genre** is the listener's favorite, it gets **2 points** — genre
  is treated as the strongest signal of taste.
- If the song's **mood** matches, it gets **1 point**.
- For **energy**, the song earns points for being *close* to the listener's target.
  A perfect match is worth a full point; the further off it is, the fewer points it
  gets. So a listener who wants calm music won't be handed the loudest track just
  because it's loud.
- A small **half-point bonus** goes to acoustic songs if the listener said they
  prefer acoustic music.

Once every song has a point total, the model simply sorts them from highest to
lowest and hands back the top few. It also keeps a short list of *reasons* for each
pick (e.g., "genre match (+2.0)") so the listener can see why a song was suggested.

**What changed from the starter:** the starter just returned the first few songs in
the file without judging them. The new version actually reads the song data as
numbers, scores every song with the point system above, ranks them, and explains
each recommendation.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The biggest weakness I found during testing is that **genre dominates everything
else**. Because a genre match is worth +2.0 while the energy score can never add
more than +1.0, the system will happily recommend a song that matches the genre
even when it badly misses the energy the user asked for. I saw this directly with
the "ambient + high energy" profile: *Spacewalk Thoughts* (an ambient track with
energy 0.28) ranked #1 for a user who requested energy 0.95, beating songs that
actually had the high energy they wanted. This creates a kind of filter bubble —
once a user names a favorite genre, songs outside that genre are almost always
pushed down, no matter how well they fit the mood or energy. The system also
ignores `valence`, `tempo_bpm`, and `danceability` entirely, and treats genre/mood
as all-or-nothing (a "pop" fan gets zero credit for an "indie pop" song), so it
can't recognize near-misses that a human listener would enjoy.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested five user profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense
Rock**, and two "adversarial" profiles with conflicting preferences — **ambient +
aggressive + high energy** and **classical + melancholy + high energy**. For each
one I ran `python -m src.main` and read the top 5 results plus the reasons the
system gave. I was mainly looking for two things: whether obvious profiles returned
songs I'd actually expect, and whether the conflicting profiles would "break" the
logic in a revealing way. The full terminal output is pasted in the README's
Experiments section.

**What surprised me:** the clean profiles behaved well and matched my intuition —
Chill Lofi returned *Library Rain* and *Midnight Coding* at the top, which is
exactly right. But the conflicting profiles exposed how strong the genre weight is.
I was surprised that a weight experiment (halving genre, doubling energy) *didn't*
change the top-5 order for the pop profile — the catalog is small enough that pop
songs are also high-energy, so the signals agree and the ranking stayed put.

**Profile comparisons (plain language):**

- **High-Energy Pop vs. Chill Lofi:** The pop profile floats upbeat, loud songs
  like *Sunrise City* and *Gym Hero* to the top; the lofi profile pulls in quiet,
  acoustic tracks like *Library Rain*. This makes sense — one asked for energy 0.9
  and the other for 0.35, so they pull toward opposite ends of the catalog.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, but swapping
  the genre from pop to rock completely changes #1 — *Sunrise City* for pop,
  *Storm Runner* for rock. It shows genre is the deciding factor whenever energy is
  similar.
- **Deep Intense Rock vs. Conflicting (ambient + high energy):** The rock profile
  gets a clean top pick because its genre, mood, and energy all point the same way.
  The ambient profile instead returns a *calm* ambient song at #1 even though the
  user asked for high energy — the genre points alone were enough to win. This is
  the clearest sign that genre is over-weighted.
- **Why "Gym Hero" keeps showing up for a Happy Pop fan:** *Gym Hero* is tagged
  pop with very high energy (0.93). A happy-pop fan asks for pop (+2.0) and high
  energy (nearly a full point), so even though its mood is "intense," not "happy,"
  it still scores high enough to sit near the top. In plain terms: it wins on two
  of the three things the user cares about, and the one it misses (mood) isn't worth
  enough points to knock it down.

No numeric accuracy metrics were computed; evaluation was done by inspecting ranked
output and reasons for each profile.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
