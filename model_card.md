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

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
