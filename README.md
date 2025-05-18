
# 🎬 Movie Picker

Welcome to Movie Picker — a smart, terminal-based app that helps you explore the best movies in your personal collection.

Whether you're in the mood for something random, want to browse by genre, or search by your favorite director or actor — Movie Picker has you covered.

# 🚀 Features

🎥 Pick a random movie from a curated list

🎭 Filter movies by genre

🎬 Search all movies by director or actor

📎 Automatically log what you’ve watched

❤️ Mark favorites for rewatch later

🔁 Stay in any mode and pick multiple times without restarting

✍️ Uses enriched JSON data with directors, genres, cast, and year


# 📂 Project Structure

MoviePicker/
├── moviepicker.py              # Main app
├── metadata_enricher.py        # Fills in metadata from TMDb
├── enrich.sh                   # CLI script to enrich movie lists
├── .env                        # TMDb API key (ignored by Git)
├── .gitignore                  # Excludes .env, __pycache__, etc.
├── history.txt                 # Watch history log
├── README.md                   # Project documentation
└── lists/                      # JSON files for movie data
    ├── plex_movies_final.json
    ├── standardized_movies_final.json
    ├── plex_movies_enriched.json
    └── standardized_movies_enriched.json

# 🛠️ Installation

1. Clone or download the project.

2. Install dependencies:
   pip install colorama python-dotenv

3. Add your TMDb API key to a .env file:
   TMDB_API_KEY=your_api_key_here

(Optional) Run enrichment:
    ./enrich.sh

# 🎯 How to Use

Choose from:

1: Pick randomly from Greatest Movies

2: Pick randomly from Plex Movies

3: Pick by Genre

4: View your Watch History

5: Reset your Watch History

6: Rewatch a Favorite

7: Search movies by Director

8: Search movies by Actor

# ✨ Example Output

🎥 Welcome to Movie Picker!

🎬 Movie of the Day
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎞️  Title    : The Thing
🎬  Director : John Carpenter
📅  Year     : 1982
🎭  Genres   : Horror, Mystery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💖 Mark this as a favorite? (y/n): y
🔁 Pick another? (y/n): n

# 💡 Future Ideas

⭐️ Add personal ratings

🖼️ Show posters and images via TMDb

📁 Export search results to .txt or .csv

🌐 GUI version using Tkinter or Flask

🧠 “Surprise Me” mode with full randomness

# 📝 License

Open source and free to use.Built for fun, film, and exploration.

# 🤝 Contributing

Pull requests welcome!Add movie data, new features, or better search tools.