"""Unit tests for CLI interface."""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import datetime

from src.ui.cli_interface import (
    CLIInterface,
    load_movies,
    fallback,
    pick_random_movie,
    pick_movie_by_genres,
    show_movie,
    pick_movie_of_the_day,
    log_movie_to_history,
)
from src.core.models import Movie


class TestCLIHelperFunctions:
    """Test helper functions in CLI interface."""

    def test_load_movies(self):
        """Test loading movies from JSON file."""
        mock_data = [
            {"title": "Test Movie", "year": 2023, "director": "Test Director"},
            {"title": "Another Movie", "year": 2022, "director": "Another Director"},
        ]

        with patch(
            "builtins.open",
            mock_open(read_data='[{"title": "Test Movie", "year": 2023}]'),
        ):
            with patch("json.load", return_value=mock_data):
                movies = load_movies("test.json")
                assert len(movies) == 2
                assert movies[0]["title"] == "Test Movie"

    def test_fallback_values(self):
        """Test fallback function for missing values."""
        assert fallback("Valid Director", "director") == "Valid Director"
        assert fallback("", "director") == "Unknown Director"
        assert fallback("unknown", "director") == "Unknown Director"
        assert fallback(None, "year") == "Unknown Year"
        assert fallback("", "genres") == "Unknown Genres"
        assert fallback("Valid Value", "other") == "Valid Value"

    def test_pick_random_movie(self):
        """Test picking random movie from unseen list."""
        movies = [{"title": "Movie 1"}, {"title": "Movie 2"}, {"title": "Movie 3"}]
        seen_titles = {"Movie 1"}

        with patch("random.choice") as mock_choice:
            mock_choice.return_value = {"title": "Movie 2"}
            movie = pick_random_movie(movies, seen_titles)
            assert movie["title"] == "Movie 2"
            # Should only choose from unseen movies
            mock_choice.assert_called_once_with(
                [{"title": "Movie 2"}, {"title": "Movie 3"}]
            )

        # Test when all movies seen
        seen_titles_all = {"Movie 1", "Movie 2", "Movie 3"}
        with patch("builtins.print") as mock_print:
            movie = pick_random_movie(movies, seen_titles_all)
            assert movie is None
            mock_print.assert_called_with(
                "\n✅ You've gone through all movies in this list!"
            )

    def test_pick_movie_by_genres(self):
        """Test picking movie by genre preferences."""
        movies = [
            {"title": "Action Movie", "genres": "Action, Thriller"},
            {"title": "Comedy Movie", "genres": "Comedy"},
            {"title": "Action Comedy", "genres": "Action, Comedy, Adventure"},
        ]
        seen_titles = set()

        # Test strict matching
        with patch("random.choice") as mock_choice:
            with patch("builtins.print"):
                mock_choice.return_value = {"title": "Action Comedy"}
                movie = pick_movie_by_genres(movies, ["Action", "Comedy"], seen_titles)
                assert movie["title"] == "Action Comedy"
                assert "Action Comedy" in seen_titles

        # Test no matches
        with patch("builtins.print") as mock_print:
            movie = pick_movie_by_genres(movies, ["Horror"], set())
            assert movie is None
            mock_print.assert_called_with("❌ No movies found for those genres.")

    @patch("builtins.print")
    def test_show_movie(self, mock_print):
        """Test displaying movie information."""
        movie = {
            "title": "Test Movie",
            "director": "Test Director",
            "year": "2023",  # Use string to avoid type error in fallback
            "genres": "Action, Comedy",
        }

        show_movie(movie, "Custom Header")

        # Verify movie details were printed
        print_calls = mock_print.call_args_list
        assert any("Custom Header" in str(call) for call in print_calls)
        assert any("Test Movie" in str(call) for call in print_calls)
        assert any("Test Director" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_show_movie_none(self, mock_print):
        """Test showing movie when None."""
        show_movie(None)
        mock_print.assert_called_with("\n❌ No movie to display.")

    def test_pick_movie_of_the_day(self):
        """Test picking movie of the day with consistent seeding."""
        movies = [{"title": "Movie 1"}, {"title": "Movie 2"}]

        with patch("random.choice") as mock_choice:
            with patch("random.seed") as mock_seed:
                with patch("src.ui.cli_interface.datetime.date") as mock_date:
                    mock_today = MagicMock()
                    mock_today.toordinal.return_value = 123456
                    mock_date.today.return_value = mock_today
                    mock_choice.return_value = {"title": "Movie 1"}

                    movie = pick_movie_of_the_day(movies)

                    assert movie["title"] == "Movie 1"
                    mock_seed.assert_called_once_with(123456)
                    mock_choice.assert_called_once_with(movies)

    def test_log_movie_to_history(self):
        """Test logging movie to history file."""
        movie = {
            "title": "Test Movie",
            "year": "2023",  # Use string to avoid type error in fallback
            "director": "Test Director",
            "genres": "Action",
        }

        with patch("builtins.open", mock_open()) as mock_file:
            with patch("src.ui.cli_interface.datetime.date") as mock_date:
                # Create a mock date that formats correctly
                mock_today = MagicMock()
                mock_today.__str__ = lambda self: "2023-01-15"
                mock_date.today.return_value = mock_today

                log_movie_to_history(movie, favorite=True)

                mock_file.assert_called_once_with("history.txt", "a", encoding="utf-8")
                written_content = mock_file().write.call_args[0][0]
                assert "2023-01-15" in written_content
                assert "Test Movie" in written_content
                assert "❤️" in written_content  # Favorite marker


class TestCLIInterface:
    """Test CLIInterface class methods."""

    @pytest.fixture
    def cli_interface(self):
        """Create CLI interface instance."""
        return CLIInterface()

    @pytest.fixture
    def sample_movie(self):
        """Create sample movie for testing."""
        return Movie(
            id=1,
            title="Test Movie",
            director="Test Director",
            year=2023,
            genres="Action, Comedy",
            rating=8.5,
            runtime=120,
            cast="Actor 1, Actor 2",
            overview="A test movie overview",
            language="en",
            country="US",
        )

    @patch("builtins.print")
    def test_display_movie_basic(self, mock_print, cli_interface, sample_movie):
        """Test basic movie display."""
        cli_interface.display_movie(sample_movie)

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "Test Movie" in printed_output
        assert "Test Director" in printed_output
        assert "8.5/10" in printed_output

    @patch("builtins.print")
    def test_display_movie_with_details(self, mock_print, cli_interface, sample_movie):
        """Test movie display with details."""
        cli_interface.display_movie(sample_movie, show_details=True)

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "Actor 1, Actor 2" in printed_output
        assert "A test movie overview" in printed_output
        assert "Language: en" in printed_output
        assert "Country: US" in printed_output

    @patch("builtins.print")
    def test_display_movie_list_empty(self, mock_print, cli_interface):
        """Test displaying empty movie list."""
        cli_interface.display_movie_list([], "Test Movies")
        mock_print.assert_called_with("\n❌ No test movies found.")

    @patch("builtins.print")
    def test_display_movie_list(self, mock_print, cli_interface, sample_movie):
        """Test displaying movie list."""
        movies = [sample_movie]
        cli_interface.display_movie_list(movies, "Test Movies")

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "Test Movies (1 found)" in printed_output
        assert "Test Movie (2023) - 8.5/10" in printed_output
        assert "Director: Test Director" in printed_output

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_user_choice_valid(self, mock_print, mock_input, cli_interface):
        """Test getting valid user choice."""
        mock_input.return_value = "2"
        choice = cli_interface.get_user_choice("Choose: ", 5)
        assert choice == 2

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_user_choice_quit(self, mock_print, mock_input, cli_interface):
        """Test quitting from user choice."""
        mock_input.return_value = "q"
        choice = cli_interface.get_user_choice("Choose: ", 5)
        assert choice is None

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_user_choice_invalid_then_valid(
        self, mock_print, mock_input, cli_interface
    ):
        """Test invalid input followed by valid input."""
        mock_input.side_effect = ["invalid", "10", "3"]
        choice = cli_interface.get_user_choice("Choose: ", 5)
        assert choice == 3

        # Should print error messages for invalid inputs
        error_calls = [call for call in mock_print.call_args_list if "❌" in str(call)]
        assert len(error_calls) == 2  # Two error messages

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_search_movies(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test searching movies."""
        mock_input.return_value = "test query"
        mock_movie_manager.search_movies.return_value = [sample_movie]

        cli_interface.search_movies()

        mock_movie_manager.search_movies.assert_called_once_with("test query")
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Search Results for 'test query'" in printed_output

    @patch("builtins.input")
    @patch("builtins.print")
    def test_search_movies_empty_query(self, mock_print, mock_input, cli_interface):
        """Test search with empty query."""
        mock_input.return_value = ""
        cli_interface.search_movies()
        mock_print.assert_called_with("❌ Please enter a search term")

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_browse_by_genre(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test browsing by genre."""
        mock_input.return_value = "Action"
        mock_movie_manager.get_movies_by_genre.return_value = [sample_movie]

        cli_interface.browse_by_genre()

        mock_movie_manager.get_movies_by_genre.assert_called_once_with("Action")
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movies in Action genre" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_top_rated(
        self, mock_print, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test showing top rated movies."""
        mock_movie_manager.get_top_rated_movies.return_value = [sample_movie]

        cli_interface.show_top_rated()

        mock_movie_manager.get_top_rated_movies.assert_called_once()
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Top Rated Movies" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_recent_movies(
        self, mock_print, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test showing recent movies."""
        mock_movie_manager.get_recent_movies.return_value = [sample_movie]

        cli_interface.show_recent_movies()

        mock_movie_manager.get_recent_movies.assert_called_once()
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Recent Movies" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_filter_by_year(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test filtering by year range."""
        mock_input.side_effect = ["2020", "2023"]
        mock_movie_manager.advanced_filter.return_value = [sample_movie]

        cli_interface.filter_by_year()

        mock_movie_manager.advanced_filter.assert_called_once_with(
            year_min=2020, year_max=2023, limit=20
        )
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movies from 2020 to 2023" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_filter_by_rating(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test filtering by rating range."""
        mock_input.side_effect = ["8.0", "10.0"]
        mock_movie_manager.advanced_filter.return_value = [sample_movie]

        cli_interface.filter_by_rating()

        mock_movie_manager.advanced_filter.assert_called_once_with(
            rating_min=8.0,
            rating_max=10.0,
            order_by="rating",
            order_direction="desc",
            limit=20,
        )
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movies rated 8.0 to 10.0" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_filter_by_genre_input(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test filtering by genre."""
        mock_input.return_value = "Action"
        mock_movie_manager.advanced_filter.return_value = [sample_movie]

        cli_interface.filter_by_genre()

        mock_movie_manager.advanced_filter.assert_called_once_with(
            genres=["Action"], limit=20
        )
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movies in Action genre" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_filter_by_director(
        self, mock_print, mock_input, mock_movie_manager, cli_interface, sample_movie
    ):
        """Test filtering by director."""
        mock_input.return_value = "Christopher Nolan"
        mock_movie_manager.advanced_filter.return_value = [sample_movie]

        cli_interface.filter_by_director()

        mock_movie_manager.advanced_filter.assert_called_once_with(
            directors=["Christopher Nolan"], limit=20
        )
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movies by Christopher Nolan" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_filter_stats(self, mock_print, mock_movie_manager, cli_interface):
        """Test showing filter statistics."""
        mock_stats = {
            "total_movies": 100,
            "year_range": {"min": 1990, "max": 2023},
            "rating_range": {"min": 1.0, "max": 10.0, "average": 7.5},
            "runtime_range": {"min": 60, "max": 180, "average": 120},
            "available_genres": ["Action", "Comedy", "Drama"],
            "available_languages": ["en", "es", "fr"],
        }
        mock_movie_manager.get_filter_stats.return_value = mock_stats

        cli_interface.show_filter_stats()

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "Total Movies: 100" in printed_output
        assert "Year Range: 1990 - 2023" in printed_output
        assert "Average Rating: 7.5" in printed_output
        assert "Action, Comedy, Drama" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("src.ui.cli_interface.datetime")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_show_movie_of_the_day(
        self,
        mock_print,
        mock_input,
        mock_datetime,
        mock_movie_manager,
        cli_interface,
        sample_movie,
    ):
        """Test showing movie of the day."""
        mock_datetime.now.return_value.strftime.return_value = "January 15, 2023"
        mock_movie_manager.get_movie_of_the_day.return_value = sample_movie
        mock_input.side_effect = ["n"]  # Don't mark as watched

        cli_interface.show_movie_of_the_day()

        mock_movie_manager.get_movie_of_the_day.assert_called_once()
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "MOVIE OF THE DAY - January 15, 2023" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("src.ui.cli_interface.datetime")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_show_movie_of_the_day_mark_watched(
        self,
        mock_print,
        mock_input,
        mock_datetime,
        mock_movie_manager,
        cli_interface,
        sample_movie,
    ):
        """Test marking movie of the day as watched."""
        mock_datetime.now.return_value.strftime.return_value = "January 15, 2023"
        mock_movie_manager.get_movie_of_the_day.return_value = sample_movie
        mock_movie_manager.mark_as_watched.return_value = True
        mock_input.side_effect = ["y", "8.5"]  # Mark as watched with rating

        cli_interface.show_movie_of_the_day()

        mock_movie_manager.mark_as_watched.assert_called_once_with(1, rating=8.5)
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)
        assert "Movie marked as watched!" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_watch_history(self, mock_print, mock_movie_manager, cli_interface):
        """Test showing watch history."""
        mock_history = [
            {
                "movie": {"title": "Test Movie", "year": 2023},
                "watched_at": datetime.datetime(2023, 1, 15, 20, 30),
                "rating": 8,
            }
        ]
        mock_movie_manager.get_watch_history.return_value = mock_history

        cli_interface.show_watch_history()

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "WATCH HISTORY" in printed_output
        assert "Test Movie (2023)" in printed_output
        assert "2023-01-15 20:30" in printed_output
        assert "Your Rating: 8/10" in printed_output

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_watch_history_empty(
        self, mock_print, mock_movie_manager, cli_interface
    ):
        """Test showing empty watch history."""
        mock_movie_manager.get_watch_history.return_value = []

        cli_interface.show_watch_history()

        mock_print.assert_called_with("❌ No watch history found")

    @patch("src.ui.cli_interface.movie_manager")
    @patch("builtins.print")
    def test_show_statistics(self, mock_print, mock_movie_manager, cli_interface):
        """Test showing user statistics."""
        mock_history = [
            {
                "movie": {
                    "title": "Movie 1",
                    "year": 2023,
                    "genres": "Action, Thriller",
                },
                "watched_at": datetime.datetime.now(),
                "rating": 8,
            },
            {
                "movie": {"title": "Movie 2", "year": 2022, "genres": "Comedy"},
                "watched_at": datetime.datetime.now(),
                "rating": 7,
            },
        ]
        mock_movie_manager.get_watch_history.return_value = mock_history

        cli_interface.show_statistics()

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "YOUR STATISTICS" in printed_output
        assert "Total Movies Watched: 2" in printed_output
        assert "Average Rating Given: 7.5/10" in printed_output
        assert "Top Genres:" in printed_output

    @patch("builtins.print")
    def test_show_about(self, mock_print, cli_interface):
        """Test showing about information."""
        cli_interface.show_about()

        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = " ".join(print_calls)

        assert "ABOUT MOVIEPICKER" in printed_output
        assert "Personalized recommendations" in printed_output
        assert "Watch history tracking" in printed_output


class TestCLIMainFunction:
    """Test main CLI functions and error handling."""

    @patch("src.ui.cli_interface.CLIInterface")
    @patch("builtins.print")
    def test_main_keyboard_interrupt(self, mock_print, mock_cli_class):
        """Test handling KeyboardInterrupt."""
        from src.ui.cli_interface import main

        mock_cli = mock_cli_class.return_value
        mock_cli.run.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_print.assert_called_with("\n\n👋 Goodbye!")

    @patch("src.ui.cli_interface.CLIInterface")
    @patch("src.ui.cli_interface.logger")
    @patch("builtins.print")
    def test_main_exception(self, mock_print, mock_logger, mock_cli_class):
        """Test handling general exception."""
        from src.ui.cli_interface import main

        mock_cli = mock_cli_class.return_value
        mock_cli.run.side_effect = Exception("Test error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_with("CLI error: Test error")
        mock_print.assert_called_with("❌ An error occurred: Test error")
