import json
import random
import datetime
import sys
from pathlib import Path
from colorama import Fore, Style, init
from typing import List, Optional

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import the new movie manager
from src.core.movie_manager import movie_manager
from src.core.models import Movie
from src.utils.logger import get_logger

# Initialize colorama to auto-reset colors after each print
init(autoreset=True)

logger = get_logger(__name__)


# Load movie data from a specified JSON file path
# Returns a list of movie dictionaries
def load_movies(filepath):
    """Load the movie list from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# Provides fallback values for missing or unknown metadata fields
# Used to display consistent default labels in the UI
def fallback(value, field_name):
    """Fallback for missing fields."""
    if not value or value.lower() == "unknown":
        if field_name == "director":
            return "Unknown Director"
        elif field_name == "year":
            return "Unknown Year"
        elif field_name == "genres":
            return "Unknown Genres"
    return value


# Pick a random movie from a list that has not yet been seen in this session
# Adds the selected movie to the seen_titles set to avoid repeats
def pick_random_movie(movies, seen_titles):
    """Pick a random movie that hasn't been seen yet in this session."""
    unseen = [m for m in movies if m["title"] not in seen_titles]
    if not unseen:
        print("\n✅ You've gone through all movies in this list!")
        return None
    movie = random.choice(unseen)
    return movie


# Pick a movie by genre preferences
# Tries strict matching first (all genres match), then falls back to partial match (any genre matches)
def pick_movie_by_genres(movies, desired_genres, seen_titles):
    """Pick a random movie matching desired genres and not already seen."""
    # First: strict AND matching
    strict_matches = []
    for movie in movies:
        if movie["title"] in seen_titles:
            continue
        movie_genres = [
            g.strip().lower()
            for g in fallback(movie.get("genres", ""), "genres").split(",")
        ]
        if all(genre.lower() in movie_genres for genre in desired_genres):
            strict_matches.append(movie)

    if strict_matches:
        print("\n✅ Found a perfect match!")
        picked = random.choice(strict_matches)
        seen_titles.add(picked["title"])
        return picked

    # If no strict matches: fallback to OR matching
    print("\n⚠️ No perfect match found. Trying partial matches...")
    loose_matches = []
    for movie in movies:
        if movie["title"] in seen_titles:
            continue
        movie_genres = [
            g.strip().lower()
            for g in fallback(movie.get("genres", ""), "genres").split(",")
        ]
        if any(genre.lower() in movie_genres for genre in desired_genres):
            loose_matches.append(movie)

    if loose_matches:
        picked = random.choice(loose_matches)
        seen_titles.add(picked["title"])
        return picked

    print("❌ No movies found for those genres.")
    return None


# Display a selected movie's information in a formatted terminal output
def show_movie(movie, header="Movie Picked!"):
    """Display movie details cleanly and professionally."""
    if not movie:
        print("\n❌ No movie to display.")
        return

    title = fallback(movie.get("title", "Unknown Title"), "title")
    director = fallback(movie.get("director", ""), "director")
    year = fallback(movie.get("year", ""), "year")
    genres = fallback(movie.get("genres", ""), "genres")

    print("\n" + "━" * 60)
    print(f"🎬 {Fore.CYAN}{Style.BRIGHT}{header}{Style.RESET_ALL}")
    print("━" * 60)
    print(f"🎞️  {Fore.BLUE}Title    :{Style.RESET_ALL} {title}")
    print(f"🎬 {Fore.YELLOW}Director :{Style.RESET_ALL} {director}")
    print(f"📅 {Fore.GREEN}Year     :{Style.RESET_ALL} {year}")
    print(f"🎭 {Fore.MAGENTA}Genres   :{Style.RESET_ALL} {genres}")
    print("━" * 60)
    print()  # Blank line after movie


# Picks a "Movie of the Day" by seeding the random generator with today's date
# Ensures a consistent pick for the same day
def pick_movie_of_the_day(movies):
    """Pick a movie of the day based on today's date."""
    today = datetime.date.today()
    random.seed(today.toordinal())  # Use the date to create a fixed seed
    return random.choice(movies)


# Logs a selected movie to history.txt with a timestamp and optional favorite flag
# Each log entry includes title, year, director, genres, and a heart if favorited
def log_movie_to_history(movie, favorite=False):
    """Append the picked movie to a history file with timestamp."""
    if not movie:
        return
    fav_mark = " ❤️" if favorite else ""
    with open("history.txt", "a", encoding="utf-8") as f:
        line = f"{datetime.date.today()} | {fallback(movie.get('title'), 'title')} ({fallback(movie.get('year'), 'year')}) | {fallback(movie.get('director'), 'director')} | {fallback(movie.get('genres'), 'genres')}{fav_mark}\n"
        f.write(line)


class CLIInterface:
    """Command-line interface for MoviePicker."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def display_movie(self, movie: Movie, show_details: bool = False):
        """Display movie information."""
        print(f"\n🎬 {movie.title} ({movie.year})")
        print(f"📽️  Director: {movie.director}")
        print(f"⭐ Rating: {movie.rating}/10" if movie.rating else "⭐ Rating: N/A")
        print(
            f"⏱️  Runtime: {movie.runtime} min" if movie.runtime else "⏱️  Runtime: N/A"
        )
        print(f"🎭 Genres: {movie.genres}" if movie.genres else "🎭 Genres: N/A")

        if show_details:
            if movie.cast:
                print(f"👥 Cast: {movie.cast}")
            if movie.overview:
                print(f"📝 Overview: {movie.overview}")
            if movie.language:
                print(f"🌍 Language: {movie.language}")
            if movie.country:
                print(f"🌎 Country: {movie.country}")

    def display_movie_list(self, movies: List[Movie], title: str = "Movies"):
        """Display a list of movies."""
        if not movies:
            print(f"\n❌ No {title.lower()} found.")
            return

        print(f"\n📋 {title} ({len(movies)} found):")
        print("=" * 60)

        for i, movie in enumerate(movies, 1):
            print(
                f"{i:2d}. {movie.title} ({movie.year}) - {movie.rating}/10"
                if movie.rating
                else f"{i:2d}. {movie.title} ({movie.year}) - N/A"
            )
            if movie.director:
                print(f"    Director: {movie.director}")
            if movie.genres:
                print(f"    Genres: {movie.genres}")
            print()

    def get_user_choice(self, prompt: str, max_choice: int) -> Optional[int]:
        """Get user choice with validation."""
        while True:
            try:
                choice = input(prompt).strip()
                if choice.lower() in ["q", "quit", "exit"]:
                    return None

                choice_num = int(choice)
                if 1 <= choice_num <= max_choice:
                    return choice_num
                else:
                    print(f"❌ Please enter a number between 1 and {max_choice}")
            except ValueError:
                print("❌ Please enter a valid number")

    def advanced_filter_menu(self):
        """Advanced filtering menu."""
        while True:
            print("\n🔍 ADVANCED FILTERING")
            print("=" * 40)
            print("1. Filter by Year Range")
            print("2. Filter by Rating Range")
            print("3. Filter by Runtime")
            print("4. Filter by Genre")
            print("5. Filter by Director")
            print("6. Filter by Actor")
            print("7. Filter by Language")
            print("8. Filter by Country")
            print("9. Multi-Criteria Filter")
            print("10. View Filter Statistics")
            print("0. Back to Main Menu")

            choice = self.get_user_choice("\nSelect an option: ", 10)

            if choice is None:
                return

            if choice == 0:
                break
            elif choice == 1:
                self.filter_by_year()
            elif choice == 2:
                self.filter_by_rating()
            elif choice == 3:
                self.filter_by_runtime()
            elif choice == 4:
                self.filter_by_genre()
            elif choice == 5:
                self.filter_by_director()
            elif choice == 6:
                self.filter_by_actor()
            elif choice == 7:
                self.filter_by_language()
            elif choice == 8:
                self.filter_by_country()
            elif choice == 9:
                self.multi_criteria_filter()
            elif choice == 10:
                self.show_filter_stats()

    def filter_by_year(self):
        """Filter movies by year range."""
        try:
            print("\n📅 Filter by Year Range")
            print("Enter year range (leave empty to skip):")

            year_min = input("From year: ").strip()
            year_max = input("To year: ").strip()

            year_min = int(year_min) if year_min else None
            year_max = int(year_max) if year_max else None

            movies = movie_manager.advanced_filter(
                year_min=year_min, year_max=year_max, limit=20
            )

            self.display_movie_list(
                movies, f"Movies from {year_min or 'any'} to {year_max or 'any'}"
            )

        except ValueError:
            print("❌ Please enter valid years")

    def filter_by_rating(self):
        """Filter movies by rating range."""
        try:
            print("\n⭐ Filter by Rating Range")
            print("Enter rating range (1-10, leave empty to skip):")

            rating_min = input("Minimum rating: ").strip()
            rating_max = input("Maximum rating: ").strip()

            rating_min = float(rating_min) if rating_min else None
            rating_max = float(rating_max) if rating_max else None

            movies = movie_manager.advanced_filter(
                rating_min=rating_min,
                rating_max=rating_max,
                order_by="rating",
                order_direction="desc",
                limit=20,
            )

            self.display_movie_list(
                movies, f"Movies rated {rating_min or 'any'} to {rating_max or 'any'}"
            )

        except ValueError:
            print("❌ Please enter valid ratings")

    def filter_by_runtime(self):
        """Filter movies by runtime."""
        try:
            print("\n⏱️  Filter by Runtime")
            print("Enter runtime range in minutes (leave empty to skip):")

            runtime_min = input("Minimum runtime: ").strip()
            runtime_max = input("Maximum runtime: ").strip()

            runtime_min = int(runtime_min) if runtime_min else None
            runtime_max = int(runtime_max) if runtime_max else None

            movies = movie_manager.advanced_filter(
                runtime_min=runtime_min, runtime_max=runtime_max, limit=20
            )

            self.display_movie_list(
                movies,
                f"Movies {runtime_min or 'any'} to {runtime_max or 'any'} minutes",
            )

        except ValueError:
            print("❌ Please enter valid runtime values")

    def filter_by_genre(self):
        """Filter movies by genre."""
        print("\n🎭 Filter by Genre")
        genre = input("Enter genre: ").strip()

        if genre:
            movies = movie_manager.advanced_filter(genres=[genre], limit=20)
            self.display_movie_list(movies, f"Movies in {genre} genre")
        else:
            print("❌ Please enter a genre")

    def filter_by_director(self):
        """Filter movies by director."""
        print("\n📽️  Filter by Director")
        director = input("Enter director name: ").strip()

        if director:
            movies = movie_manager.advanced_filter(directors=[director], limit=20)
            self.display_movie_list(movies, f"Movies by {director}")
        else:
            print("❌ Please enter a director name")

    def filter_by_actor(self):
        """Filter movies by actor."""
        print("\n👥 Filter by Actor")
        actor = input("Enter actor name: ").strip()

        if actor:
            movies = movie_manager.advanced_filter(actors=[actor], limit=20)
            self.display_movie_list(movies, f"Movies featuring {actor}")
        else:
            print("❌ Please enter an actor name")

    def filter_by_language(self):
        """Filter movies by language."""
        print("\n🌍 Filter by Language")
        language = input("Enter language: ").strip()

        if language:
            movies = movie_manager.advanced_filter(languages=[language], limit=20)
            self.display_movie_list(movies, f"Movies in {language}")
        else:
            print("❌ Please enter a language")

    def filter_by_country(self):
        """Filter movies by country."""
        print("\n🌎 Filter by Country")
        country = input("Enter country: ").strip()

        if country:
            movies = movie_manager.advanced_filter(countries=[country], limit=20)
            self.display_movie_list(movies, f"Movies from {country}")
        else:
            print("❌ Please enter a country")

    def multi_criteria_filter(self):
        """Multi-criteria filtering."""
        print("\n🔍 Multi-Criteria Filter")
        print("Enter criteria (leave empty to skip):")

        try:
            # Year range
            year_min = input("From year: ").strip()
            year_max = input("To year: ").strip()
            year_min = int(year_min) if year_min else None
            year_max = int(year_max) if year_max else None

            # Rating range
            rating_min = input("Minimum rating (1-10): ").strip()
            rating_max = input("Maximum rating (1-10): ").strip()
            rating_min = float(rating_min) if rating_min else None
            rating_max = float(rating_max) if rating_max else None

            # Runtime range
            runtime_min = input("Minimum runtime (minutes): ").strip()
            runtime_max = input("Maximum runtime (minutes): ").strip()
            runtime_min = int(runtime_min) if runtime_min else None
            runtime_max = int(runtime_max) if runtime_max else None

            # Genre
            genre = input("Genre: ").strip()
            genres = [genre] if genre else None

            # Director
            director = input("Director: ").strip()
            directors = [director] if director else None

            # Actor
            actor = input("Actor: ").strip()
            actors = [actor] if actor else None

            # Language
            language = input("Language: ").strip()
            languages = [language] if language else None

            # Country
            country = input("Country: ").strip()
            countries = [country] if country else None

            # Exclude watched
            exclude_watched = (
                input("Exclude watched movies? (y/n): ").strip().lower() == "y"
            )

            movies = movie_manager.advanced_filter(
                year_min=year_min,
                year_max=year_max,
                rating_min=rating_min,
                rating_max=rating_max,
                runtime_min=runtime_min,
                runtime_max=runtime_max,
                genres=genres,
                directors=directors,
                actors=actors,
                languages=languages,
                countries=countries,
                exclude_watched=exclude_watched,
                limit=20,
            )

            self.display_movie_list(movies, "Filtered Movies")

        except ValueError:
            print("❌ Please enter valid values")

    def show_filter_stats(self):
        """Show filtering statistics."""
        stats = movie_manager.get_filter_stats()

        print("\n📊 FILTER STATISTICS")
        print("=" * 40)
        print(f"Total Movies: {stats['total_movies']}")

        if "year_range" in stats:
            print(
                f"Year Range: {stats['year_range']['min']} - {stats['year_range']['max']}"
            )

        if "rating_range" in stats:
            print(
                f"Rating Range: {stats['rating_range']['min']:.1f} - {stats['rating_range']['max']:.1f}"
            )
            print(f"Average Rating: {stats['rating_range']['average']:.1f}")

        if "runtime_range" in stats:
            print(
                f"Runtime Range: {stats['runtime_range']['min']} - {stats['runtime_range']['max']} minutes"
            )
            print(f"Average Runtime: {stats['runtime_range']['average']:.0f} minutes")

        if "available_genres" in stats:
            print(f"Available Genres: {', '.join(stats['available_genres'][:10])}")
            if len(stats["available_genres"]) > 10:
                print(f"  ... and {len(stats['available_genres']) - 10} more")

        if "available_languages" in stats:
            print(
                f"Available Languages: {', '.join(stats['available_languages'][:10])}"
            )
            if len(stats["available_languages"]) > 10:
                print(f"  ... and {len(stats['available_languages']) - 10} more")

    def search_and_discover_menu(self):
        """Search and discover menu."""
        while True:
            print("\n🔍 SEARCH & DISCOVER")
            print("=" * 30)
            print("1. Search Movies")
            print("2. Browse by Genre")
            print("3. Top Rated Movies")
            print("4. Recent Movies")
            print("5. Advanced Filtering")
            print("0. Back to Main Menu")

            choice = self.get_user_choice("\nSelect an option: ", 5)

            if choice is None:
                return

            if choice == 0:
                break
            elif choice == 1:
                self.search_movies()
            elif choice == 2:
                self.browse_by_genre()
            elif choice == 3:
                self.show_top_rated()
            elif choice == 4:
                self.show_recent_movies()
            elif choice == 5:
                self.advanced_filter_menu()

    def search_movies(self):
        """Search movies."""
        query = input("\n🔍 Enter search term: ").strip()
        if query:
            movies = movie_manager.search_movies(query)
            self.display_movie_list(movies, f"Search Results for '{query}'")
        else:
            print("❌ Please enter a search term")

    def browse_by_genre(self):
        """Browse movies by genre."""
        genre = input("\n🎭 Enter genre: ").strip()
        if genre:
            movies = movie_manager.get_movies_by_genre(genre)
            self.display_movie_list(movies, f"Movies in {genre} genre")
        else:
            print("❌ Please enter a genre")

    def show_top_rated(self):
        """Show top rated movies."""
        movies = movie_manager.get_top_rated_movies()
        self.display_movie_list(movies, "Top Rated Movies")

    def show_recent_movies(self):
        """Show recent movies."""
        movies = movie_manager.get_recent_movies()
        self.display_movie_list(movies, "Recent Movies")

    def pick_a_movie_menu(self):
        """Pick a movie menu."""
        while True:
            print("\n🎲 PICK A MOVIE")
            print("=" * 20)
            print("1. Movie of the Day")
            print("2. Random Movie")
            print("3. Personalized Recommendations")
            print("4. Surprise Me!")
            print("0. Back to Main Menu")

            choice = self.get_user_choice("\nSelect an option: ", 4)

            if choice is None:
                return

            if choice == 0:
                break
            elif choice == 1:
                self.show_movie_of_the_day()
            elif choice == 2:
                self.pick_random_movie()
            elif choice == 3:
                self.show_recommendations()
            elif choice == 4:
                self.surprise_me()

    def show_movie_of_the_day(self):
        """Show movie of the day."""
        movie = movie_manager.get_movie_of_the_day()
        if movie:
            print(f"\n🎬 MOVIE OF THE DAY - {datetime.now().strftime('%B %d, %Y')}")
            print("=" * 50)
            self.display_movie(movie, show_details=True)

            choice = input("\nMark as watched? (y/n): ").strip().lower()
            if choice == "y":
                rating = input(
                    "Rate this movie (1-10, or press Enter to skip): "
                ).strip()
                try:
                    rating_val = float(rating) if rating else None
                    if movie_manager.mark_as_watched(movie.id, rating=rating_val):
                        print("✅ Movie marked as watched!")
                    else:
                        print("❌ Failed to mark movie as watched")
                except ValueError:
                    print("❌ Invalid rating")
        else:
            print("❌ No movie available for today")

    def pick_random_movie(self):
        """Pick a random movie."""
        # Use advanced filter to get unwatched movies
        movies = movie_manager.advanced_filter(exclude_watched=True, limit=1)
        if movies:
            movie = movies[0]
            print("\n🎲 RANDOM MOVIE")
            print("=" * 20)
            self.display_movie(movie, show_details=True)

            choice = input("\nMark as watched? (y/n): ").strip().lower()
            if choice == "y":
                rating = input(
                    "Rate this movie (1-10, or press Enter to skip): "
                ).strip()
                try:
                    rating_val = float(rating) if rating else None
                    if movie_manager.mark_as_watched(movie.id, rating=rating_val):
                        print("✅ Movie marked as watched!")
                    else:
                        print("❌ Failed to mark movie as watched")
                except ValueError:
                    print("❌ Invalid rating")
        else:
            print("❌ No movies available")

    def show_recommendations(self):
        """Show personalized recommendations."""
        recommendations = movie_manager.get_recommendations()

        if recommendations:
            for category, movies in recommendations.items():
                if movies:
                    print(f"\n💡 {category.upper()}")
                    print("-" * 30)
                    self.display_movie_list(movies, category.title())
        else:
            print("❌ No recommendations available. Try watching some movies first!")

    def surprise_me(self):
        """Surprise me with a random recommendation."""
        recommendations = movie_manager.get_recommendations()

        all_movies = []
        for movies in recommendations.values():
            all_movies.extend(movies)

        if all_movies:
            import random

            movie = random.choice(all_movies)
            print("\n🎉 SURPRISE MOVIE!")
            print("=" * 20)
            self.display_movie(movie, show_details=True)

            choice = input("\nMark as watched? (y/n): ").strip().lower()
            if choice == "y":
                rating = input(
                    "Rate this movie (1-10, or press Enter to skip): "
                ).strip()
                try:
                    rating_val = float(rating) if rating else None
                    if movie_manager.mark_as_watched(movie.id, rating=rating_val):
                        print("✅ Movie marked as watched!")
                    else:
                        print("❌ Failed to mark movie as watched")
                except ValueError:
                    print("❌ Invalid rating")
        else:
            print("❌ No recommendations available")

    def my_account_menu(self):
        """My account menu."""
        while True:
            print("\n👤 MY ACCOUNT")
            print("=" * 20)
            print("1. View Watch History")
            print("2. View Statistics")
            print("0. Back to Main Menu")

            choice = self.get_user_choice("\nSelect an option: ", 2)

            if choice is None:
                return

            if choice == 0:
                break
            elif choice == 1:
                self.show_watch_history()
            elif choice == 2:
                self.show_statistics()

    def show_watch_history(self):
        """Show watch history."""
        history = movie_manager.get_watch_history()

        if history:
            print("\n📺 WATCH HISTORY")
            print("=" * 30)

            for i, entry in enumerate(history, 1):
                movie = entry["movie"]
                watched_at = entry["watched_at"]
                rating = entry["rating"]

                print(f"{i:2d}. {movie['title']} ({movie['year']})")
                print(f"    Watched: {watched_at.strftime('%Y-%m-%d %H:%M')}")
                if rating:
                    print(f"    Your Rating: {rating}/10")
                print()
        else:
            print("❌ No watch history found")

    def show_statistics(self):
        """Show user statistics."""
        history = movie_manager.get_watch_history(
            limit=1000
        )  # Get all history for stats

        if history:
            total_watched = len(history)
            avg_rating = sum(
                entry["rating"] for entry in history if entry["rating"]
            ) / len([entry for entry in history if entry["rating"]])

            print("\n📊 YOUR STATISTICS")
            print("=" * 30)
            print(f"Total Movies Watched: {total_watched}")
            print(f"Average Rating Given: {avg_rating:.1f}/10")

            # Most watched genres
            genre_counts = {}
            for entry in history:
                genres = entry["movie"]["genres"]
                if genres:
                    for genre in genres.split(","):
                        genre = genre.strip()
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1

            if genre_counts:
                top_genres = sorted(
                    genre_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
                print(
                    f"Top Genres: {', '.join(f'{genre} ({count})' for genre, count in top_genres)}"
                )
        else:
            print("❌ No statistics available. Start watching movies!")

    def settings_menu(self):
        """Settings menu."""
        print("\n⚙️  SETTINGS")
        print("=" * 20)
        print("1. Database Info")
        print("2. About MoviePicker")
        print("0. Back to Main Menu")

        choice = self.get_user_choice("\nSelect an option: ", 2)

        if choice == 1:
            self.show_database_info()
        elif choice == 2:
            self.show_about()

    def show_database_info(self):
        """Show database information."""
        stats = movie_manager.get_filter_stats()

        print("\n🗄️  DATABASE INFO")
        print("=" * 30)
        print(f"Total Movies: {stats['total_movies']}")

        if "year_range" in stats:
            print(
                f"Year Range: {stats['year_range']['min']} - {stats['year_range']['max']}"
            )

        if "rating_range" in stats:
            print(
                f"Rating Range: {stats['rating_range']['min']:.1f} - {stats['rating_range']['max']:.1f}"
            )
            print(f"Average Rating: {stats['rating_range']['average']:.1f}")

    def show_about(self):
        """Show about information."""
        print("\nℹ️  ABOUT MOVIEPICKER")
        print("=" * 30)
        print("MoviePicker is a smart movie recommendation")
        print("system for your personal movie collection.")
        print("\nFeatures:")
        print("• Personalized recommendations")
        print("• Advanced filtering and search")
        print("• Watch history tracking")
        print("• Movie of the day")
        print("• Random movie picker")

    def run(self):
        """Run the CLI interface."""
        print("🎬 Welcome to MoviePicker!")
        print("Your personal movie recommendation system")

        while True:
            print("\n" + "=" * 50)
            print("🎬 MOVIEPICKER MAIN MENU")
            print("=" * 50)
            print("📋 PICK A MOVIE")
            print("  1. Movie of the Day")
            print("  2. Random Movie")
            print("  3. Personalized Recommendations")
            print("  4. Surprise Me!")
            print()
            print("🔍 SEARCH & DISCOVER")
            print("  5. Search Movies")
            print("  6. Browse by Genre")
            print("  7. Top Rated Movies")
            print("  8. Recent Movies")
            print("  9. Advanced Filtering")
            print()
            print("👤 MY ACCOUNT")
            print("  10. View Watch History")
            print("  11. View Statistics")
            print()
            print("⚙️  SETTINGS")
            print("  12. Database Info")
            print("  13. About MoviePicker")
            print()
            print("  0. Exit")

            choice = self.get_user_choice("\nSelect an option: ", 13)

            if choice is None or choice == 0:
                print("\n👋 Thanks for using MoviePicker!")
                break
            elif choice == 1:
                self.show_movie_of_the_day()
            elif choice == 2:
                self.pick_random_movie()
            elif choice == 3:
                self.show_recommendations()
            elif choice == 4:
                self.surprise_me()
            elif choice == 5:
                self.search_movies()
            elif choice == 6:
                self.browse_by_genre()
            elif choice == 7:
                self.show_top_rated()
            elif choice == 8:
                self.show_recent_movies()
            elif choice == 9:
                self.advanced_filter_menu()
            elif choice == 10:
                self.show_watch_history()
            elif choice == 11:
                self.show_statistics()
            elif choice == 12:
                self.show_database_info()
            elif choice == 13:
                self.show_about()


def main():
    """Main entry point for CLI."""
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"CLI error: {e}")
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
