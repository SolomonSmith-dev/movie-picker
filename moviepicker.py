
import json
import random
import datetime
from colorama import Fore, Style, init
init(autoreset=True)

def load_movies(filepath):
    """Load the movie list from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def fallback(value, field_name):
    """Fallback for missing fields."""
    if not value or value.lower() == 'unknown':
        if field_name == 'director':
            return 'Unknown Director'
        elif field_name == 'year':
            return 'Unknown Year'
        elif field_name == 'genres':
            return 'Unknown Genres'
    return value

def pick_random_movie(movies, seen_titles):
    """Pick a random movie that hasn't been seen yet in this session."""
    unseen = [m for m in movies if m['title'] not in seen_titles]
    if not unseen:
        print("\n✅ You've gone through all movies in this list!")
        return None
    movie = random.choice(unseen)
    seen_titles.add(movie['title'])
    return movie


def pick_movie_by_genres(movies, desired_genres, seen_titles):
    """Pick a random movie matching desired genres and not already seen."""
    # First: strict AND matching
    strict_matches = []
    for movie in movies:
        if movie['title'] in seen_titles:
            continue
        movie_genres = [g.strip().lower() for g in fallback(movie.get('genres', ''), 'genres').split(',')]
        if all(genre.lower() in movie_genres for genre in desired_genres):
            strict_matches.append(movie)

    if strict_matches:
        print(f"\n✅ Found a perfect match!")
        picked = random.choice(strict_matches)
        seen_titles.add(picked['title'])
        return picked

    # If no strict matches: fallback to OR matching
    print("\n⚠️ No perfect match found. Trying partial matches...")
    loose_matches = []
    for movie in movies:
        if movie['title'] in seen_titles:
            continue
        movie_genres = [g.strip().lower() for g in fallback(movie.get('genres', ''), 'genres').split(',')]
        if any(genre.lower() in movie_genres for genre in desired_genres):
            loose_matches.append(movie)

    if loose_matches:
        picked = random.choice(loose_matches)
        seen_titles.add(picked['title'])
        return picked

    print("❌ No movies found for those genres.")
    return None


def show_movie(movie, header="Movie Picked!"):
    """Display movie details cleanly and professionally."""
    if not movie:
        print("\n❌ No movie to display.")
        return

    title = fallback(movie.get('title', 'Unknown Title'), 'title')
    director = fallback(movie.get('director', ''), 'director')
    year = fallback(movie.get('year', ''), 'year')
    genres = fallback(movie.get('genres', ''), 'genres')

    print("\n" + "━" * 60)
    print(f"🎬 {Fore.CYAN}{Style.BRIGHT}{header}{Style.RESET_ALL}")
    print("━" * 60)
    print(f"🎞️  {Fore.BLUE}Title    :{Style.RESET_ALL} {title}")
    print(f"🎬 {Fore.YELLOW}Director :{Style.RESET_ALL} {director}")
    print(f"📅 {Fore.GREEN}Year     :{Style.RESET_ALL} {year}")
    print(f"🎭 {Fore.MAGENTA}Genres   :{Style.RESET_ALL} {genres}")
    print("━" * 60)
    print()  # Blank line after movie


def pick_movie_of_the_day(movies):
    """Pick a movie of the day based on today's date."""
    today = datetime.date.today()
    random.seed(today.toordinal())  # Use the date to create a fixed seed
    return random.choice(movies)

def log_movie_to_history(movie, favorite=False):
    """Append the picked movie to a history file with timestamp."""
    if not movie:
        return
    fav_mark = " ❤️" if favorite else ""
    with open("history.txt", "a", encoding="utf-8") as f:
        line = f"{datetime.date.today()} | {fallback(movie.get('title'), 'title')} ({fallback(movie.get('year'), 'year')}) | {fallback(movie.get('director'), 'director')} | {fallback(movie.get('genres'), 'genres')}{fav_mark}\n"
        f.write(line)

def main():
    seen_titles = set()

    # Load watched titles from history
    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            for line in f:
                title = line.split("|")[1].strip().split(" (")[0]
                seen_titles.add(title)
    except FileNotFoundError:
        pass

    greatest_movies = load_movies('lists/standardized_movies_final.json')
    plex_movies = load_movies('lists/plex_movies_final.json')
    random.shuffle(plex_movies)
    combined_movies = greatest_movies + plex_movies

    # Load enriched versions for search
    with open("lists/standardized_movies_enriched.json", "r", encoding="utf-8") as f:
        enriched_greatest = json.load(f)
    with open("lists/plex_movies_enriched.json", "r", encoding="utf-8") as f:
        enriched_plex = json.load(f)
    enriched_combined = enriched_greatest + enriched_plex

    print("\n🎥 Welcome to Movie Picker!\n")

    movie_of_the_day = pick_movie_of_the_day(combined_movies)
    show_movie(movie_of_the_day, header="Movie of the Day")

    pick_today = input("🎬 Would you like to watch the Movie of the Day? (y/n): ")
    if pick_today.lower() == 'y':
        print("\n🎉 Enjoy your Movie of the Day! Goodbye!\n")
        return

    while True:
        print("1. Pick from Greatest Movies")
        print("2. Pick from My Plex Movies")
        print("3. Pick a Movie by Genre (Combined List)")
        print("4. View Watch History")
        print("5. Reset Watch History")
        print("6. Rewatch a Favorite")
        print("7. Search Movies by Director")
        print("8. Search Movies by Actor")

        choice = input("\n🎬 What would you like to do? (1-8): ")

        if choice == '1':
            movie = pick_random_movie(greatest_movies, seen_titles)
            show_movie(movie)
            favorite = input("💖 Mark this as a favorite? (y/n): ").strip().lower() == 'y'
            log_movie_to_history(movie, favorite)

        elif choice == '2':
            movie = pick_random_movie(plex_movies, seen_titles)
            show_movie(movie)
            favorite = input("💖 Mark this as a favorite? (y/n): ").strip().lower() == 'y'
            log_movie_to_history(movie, favorite)

        elif choice == '3':
            user_input = input("\n🎬 What genres are you feeling? (comma-separated, e.g., 'Animation, Adventure')\n> ")
            desired_genres = [g.strip() for g in user_input.split(',')]
            movie = pick_movie_by_genres(combined_movies, desired_genres, seen_titles)
            show_movie(movie)
            favorite = input("💖 Mark this as a favorite? (y/n): ").strip().lower() == 'y'
            log_movie_to_history(movie, favorite)

        elif choice == '4':
            try:
                with open("history.txt", "r", encoding="utf-8") as f:
                    history = f.read()
                print("\n📜 Watch History:\n")
                print(history if history else "No history yet.")
            except FileNotFoundError:
                print("\n📜 No history file found. Watch something first!")
            continue

        elif choice == '5':
            confirm = input("⚠️ This will erase all watch history. Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                with open("history.txt", "w", encoding="utf-8") as f:
                    f.write("")
                seen_titles.clear()
                print("✅ History cleared!")
            else:
                print("❌ Cancelled. Your history is safe.")

        elif choice == '6':
            try:
                with open("history.txt", "r", encoding="utf-8") as f:
                    lines = [line for line in f if "❤️" in line]
                if not lines:
                    print("\n😔 No favorites found yet.")
                else:
                    print("\n💖 Favorites:")
                    for i, line in enumerate(lines, 1):
                        print(f"{i}. {line.strip()}")

                    index = input("\nEnter the number of the movie you want to rewatch (or press Enter to cancel): ").strip()
                    if index.isdigit():
                        index = int(index)
                        if 1 <= index <= len(lines):
                            print("\n🎬 Rewatching your pick:")
                            print(lines[index - 1].strip())
                        else:
                            print("❌ Invalid number.")
                    else:
                        print("❌ Cancelled.")
            except FileNotFoundError:
                print("\n📜 No history file found. Watch something first!")

        elif choice == '7':
            director_name = input("🎬 Enter the director's name: ").strip().lower()
            seen_titles = set()
            matches = []
            for m in enriched_combined:
                if director_name in m.get("director", "").lower():
                    if m["title"] not in seen_titles:
                        seen_titles.add(m["title"])
                        matches.append(m)
            if matches:
                print(f"\n🎬 Found {len(matches)} unique movies directed by '{director_name.title()}':\n")
                for m in matches:
                    print(f"- {m['title']} ({m['year']})")
            else:
                print("❌ No movies found for that director.")

        elif choice == '8':
            actor_name = input("🎭 Enter the actor's name: ").strip().lower()
            seen_titles = set()
            matches = []
            for m in enriched_combined:
                if actor_name in m.get("cast", "").lower():
                    if m["title"] not in seen_titles:
                        seen_titles.add(m["title"])
                        matches.append(m)
            if matches:
                print(f"\n🎭 Found {len(matches)} unique movies with '{actor_name.title()}':\n")
                for m in matches:
                    print(f"- {m['title']} ({m['year']})")
            else:
                print("❌ No movies found for that actor.")


        else:
            print("\n❌ Invalid choice.")

        again = input("🔁 Pick another movie? (y/n): ")
        if again.lower() != 'y':
            print("\n👋 Goodbye! Enjoy your movie!")
            break
        print()

if __name__ == "__main__":
    main()