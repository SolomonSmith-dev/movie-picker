"""Integration tests for MovieManager with real database operations."""

import pytest
from datetime import datetime
from unittest.mock import patch

from src.core.movie_manager import MovieManager
from src.core.models import Movie, User, WatchHistory, UserRating


@pytest.mark.integration
class TestMovieManagerIntegration:
    """Integration tests for MovieManager with database operations."""

    def test_get_movie_of_the_day_with_data(self, populated_test_db, movie_manager_with_test_db):
        """Test getting movie of the day with actual database data."""
        movie = movie_manager_with_test_db.get_movie_of_the_day()
        
        assert movie is not None
        assert isinstance(movie, Movie)
        assert movie.title is not None
        assert movie.year is not None
    
    def test_search_movies_with_data(self, populated_test_db, movie_manager_with_test_db):
        """Test searching movies with actual database data."""
        # Search for "Matrix" - should find "The Matrix"
        results = movie_manager_with_test_db.search_movies("Matrix", limit=5)
        
        assert len(results) > 0
        matrix_found = any(movie.title == "The Matrix" for movie in results)
        assert matrix_found
    
    def test_search_movies_partial_match(self, populated_test_db, movie_manager_with_test_db):
        """Test searching with partial matches."""
        # Search for "Dark" - should find "The Dark Knight"
        results = movie_manager_with_test_db.search_movies("Dark", limit=5)
        
        assert len(results) > 0
        dark_knight_found = any("Dark Knight" in movie.title for movie in results)
        assert dark_knight_found
    
    def test_get_movies_by_genre(self, populated_test_db, movie_manager_with_test_db):
        """Test getting movies by genre."""
        # Get Action movies
        action_movies = movie_manager_with_test_db.get_movies_by_genre("Action", limit=10)
        
        assert len(action_movies) > 0
        for movie in action_movies:
            assert "Action" in movie.genres
    
    def test_get_top_rated_movies(self, populated_test_db, movie_manager_with_test_db):
        """Test getting top rated movies."""
        top_movies = movie_manager_with_test_db.get_top_rated_movies(limit=3)
        
        assert len(top_movies) > 0
        # Should be ordered by rating (descending)
        for i in range(len(top_movies) - 1):
            assert top_movies[i].rating >= top_movies[i + 1].rating
    
    def test_get_recent_movies(self, populated_test_db, movie_manager_with_test_db):
        """Test getting recent movies."""
        recent_movies = movie_manager_with_test_db.get_recent_movies(limit=5)
        
        assert len(recent_movies) > 0
        # All movies should be from recent years
        current_year = datetime.now().year
        for movie in recent_movies:
            assert movie.year >= current_year - 5
    
    def test_mark_as_watched_new_movie(self, populated_test_db, movie_manager_with_test_db, sample_user, sample_movies):
        """Test marking a movie as watched for the first time."""
        user_id = sample_user.id
        movie_id = sample_movies[2].id  # The Dark Knight (not yet watched by test user)
        
        result = movie_manager_with_test_db.mark_as_watched(movie_id, user_id, rating=8.5)
        
        assert result is True
        
        # Verify watch history was created
        watch_history = populated_test_db.query(WatchHistory).filter(
            WatchHistory.user_id == user_id,
            WatchHistory.movie_id == movie_id
        ).first()
        
        assert watch_history is not None
        assert watch_history.is_favorite is False  # Default
        
        # Verify rating was created
        user_rating = populated_test_db.query(UserRating).filter(
            UserRating.user_id == user_id,
            UserRating.movie_id == movie_id
        ).first()
        
        assert user_rating is not None
        assert user_rating.rating == 8  # Should be converted to int
    
    def test_mark_as_watched_existing_movie(self, populated_test_db, movie_manager_with_test_db, sample_user, sample_movies):
        """Test updating watch status for already watched movie."""
        user_id = sample_user.id
        movie_id = sample_movies[0].id  # The Matrix (already watched by test user)
        
        # Verify the movie was already watched initially
        initial_watch = populated_test_db.query(WatchHistory).filter(
            WatchHistory.user_id == user_id,
            WatchHistory.movie_id == movie_id
        ).first()
        assert initial_watch is not None
        
        # Mark as watched again with a new rating
        result = movie_manager_with_test_db.mark_as_watched(movie_id, user_id, rating=9.5)
        
        assert result is True
        
        # Verify the rating was added/updated
        user_rating = populated_test_db.query(UserRating).filter(
            UserRating.user_id == user_id,
            UserRating.movie_id == movie_id
        ).first()
        
        assert user_rating is not None
        assert user_rating.rating == 9  # Should be converted to int
    
    def test_get_watch_history(self, populated_test_db, movie_manager_with_test_db, sample_user):
        """Test getting user watch history."""
        user_id = sample_user.id
        
        history = movie_manager_with_test_db.get_watch_history(user_id, limit=10)
        
        assert len(history) >= 2  # We added 2 entries in the fixture
        
        # Verify structure of returned data
        for entry in history:
            assert 'movie' in entry
            assert 'watched_at' in entry
            assert 'rating' in entry
            
            movie_data = entry['movie']
            assert 'id' in movie_data
            assert 'title' in movie_data
            assert 'director' in movie_data
            assert 'year' in movie_data
    
    def test_get_watch_history_empty_user(self, populated_test_db, movie_manager_with_test_db):
        """Test getting watch history for user with no history."""
        non_existent_user_id = 999
        
        history = movie_manager_with_test_db.get_watch_history(non_existent_user_id, limit=10)
        
        assert len(history) == 0
    
    def test_get_recommendations(self, populated_test_db, movie_manager_with_test_db, sample_user):
        """Test getting movie recommendations."""
        user_id = sample_user.id
        
        recommendations = movie_manager_with_test_db.get_recommendations(user_id, limit=5)
        
        assert isinstance(recommendations, dict)
        assert "Personalized" in recommendations
        assert isinstance(recommendations["Personalized"], list)
    
    def test_advanced_filter_by_year(self, populated_test_db, movie_manager_with_test_db):
        """Test advanced filtering by year range."""
        # Filter movies from 2000-2010
        movies = movie_manager_with_test_db.advanced_filter(
            year_min=2000,
            year_max=2010,
            limit=10
        )
        
        assert len(movies) > 0
        for movie in movies:
            assert 2000 <= movie.year <= 2010
    
    def test_advanced_filter_by_rating(self, populated_test_db, movie_manager_with_test_db):
        """Test advanced filtering by rating."""
        # Filter movies with rating >= 8.5
        movies = movie_manager_with_test_db.advanced_filter(
            rating_min=8.5,
            limit=10
        )
        
        assert len(movies) > 0
        for movie in movies:
            assert movie.rating >= 8.5
    
    def test_advanced_filter_by_genre(self, populated_test_db, movie_manager_with_test_db):
        """Test advanced filtering by genre."""
        # Filter Action movies
        movies = movie_manager_with_test_db.advanced_filter(
            genres=["Action"],
            limit=10
        )
        
        assert len(movies) > 0
        for movie in movies:
            assert "Action" in movie.genres
    
    def test_advanced_filter_by_director(self, populated_test_db, movie_manager_with_test_db):
        """Test advanced filtering by director."""
        # Filter Christopher Nolan movies
        movies = movie_manager_with_test_db.advanced_filter(
            directors=["Christopher Nolan"],
            limit=10
        )
        
        assert len(movies) > 0
        for movie in movies:
            assert "Christopher Nolan" in movie.director
    
    def test_advanced_filter_multiple_criteria(self, populated_test_db, movie_manager_with_test_db):
        """Test advanced filtering with multiple criteria."""
        # Filter Action movies from 2000+ with rating >= 8.0
        movies = movie_manager_with_test_db.advanced_filter(
            year_min=2000,
            rating_min=8.0,
            genres=["Action"],
            limit=10
        )
        
        for movie in movies:
            assert movie.year >= 2000
            assert movie.rating >= 8.0
            assert "Action" in movie.genres
    
    def test_advanced_filter_exclude_watched(self, populated_test_db, movie_manager_with_test_db, sample_user):
        """Test advanced filtering excluding watched movies."""
        user_id = sample_user.id
        
        # Get all movies first
        all_movies = movie_manager_with_test_db.advanced_filter(limit=10)
        
        # Get movies excluding watched ones
        unwatched_movies = movie_manager_with_test_db.advanced_filter(
            exclude_watched=True,
            user_id=user_id,
            limit=10
        )
        
        # Should have fewer movies when excluding watched ones
        assert len(unwatched_movies) <= len(all_movies)
        
        # Get watched movie IDs for this user
        watched_movies = movie_manager_with_test_db.get_watch_history(user_id, limit=100)
        watched_movie_ids = {entry['movie']['id'] for entry in watched_movies}
        
        # Verify no watched movies are in the unwatched results
        for movie in unwatched_movies:
            assert movie.id not in watched_movie_ids
    
    def test_get_filter_stats(self, populated_test_db, movie_manager_with_test_db):
        """Test getting filter statistics."""
        stats = movie_manager_with_test_db.get_filter_stats()
        
        assert isinstance(stats, dict)
        assert 'total_movies' in stats
        assert 'year_range' in stats
        assert 'rating_range' in stats
        assert 'available_genres' in stats
        
        # Verify data structure
        assert stats['total_movies'] > 0
        assert 'min' in stats['year_range']
        assert 'max' in stats['year_range']
        assert 'min' in stats['rating_range']
        assert 'max' in stats['rating_range']
        assert isinstance(stats['available_genres'], list)