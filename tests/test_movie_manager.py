"""Tests for the MovieManager class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.movie_manager import MovieManager
from src.core.models import Movie


class TestMovieManager:
    """Test cases for MovieManager."""
    
    @pytest.fixture
    def movie_manager(self):
        """Create a MovieManager instance for testing."""
        return MovieManager()
    
    @pytest.fixture
    def sample_movie(self):
        """Sample Movie object for testing."""
        movie = Movie(
            id=1,
            title="Test Movie",
            director="Test Director",
            year=2020,
            genres="Action, Adventure",
            cast="Actor 1, Actor 2",
            rating=8.5
        )
        return movie
    
    def test_movie_manager_initialization(self, movie_manager):
        """Test that MovieManager initializes correctly."""
        assert movie_manager is not None
        assert hasattr(movie_manager, 'recommendation_engine')
        assert hasattr(movie_manager, 'logger')
    
    def test_get_movie_of_the_day_exists(self, movie_manager):
        """Test that get_movie_of_the_day method exists."""
        assert hasattr(movie_manager, 'get_movie_of_the_day')
    
    def test_search_movies_exists(self, movie_manager):
        """Test that search_movies method exists."""
        assert hasattr(movie_manager, 'search_movies')
    
    def test_get_movies_by_genre_exists(self, movie_manager):
        """Test that get_movies_by_genre method exists."""
        assert hasattr(movie_manager, 'get_movies_by_genre')
    
    def test_mark_as_watched_exists(self, movie_manager):
        """Test that mark_as_watched method exists."""
        assert hasattr(movie_manager, 'mark_as_watched')
    
    def test_get_watch_history_exists(self, movie_manager):
        """Test that get_watch_history method exists."""
        assert hasattr(movie_manager, 'get_watch_history')
    
    def test_get_recommendations_exists(self, movie_manager):
        """Test that get_recommendations method exists."""
        assert hasattr(movie_manager, 'get_recommendations')
    
    def test_advanced_filter_exists(self, movie_manager):
        """Test that advanced_filter method exists."""
        assert hasattr(movie_manager, 'advanced_filter')
    
    def test_get_top_rated_movies_exists(self, movie_manager):
        """Test that get_top_rated_movies method exists."""
        assert hasattr(movie_manager, 'get_top_rated_movies')
    
    def test_get_recent_movies_exists(self, movie_manager):
        """Test that get_recent_movies method exists."""
        assert hasattr(movie_manager, 'get_recent_movies')
    
    def test_get_filter_stats_exists(self, movie_manager):
        """Test that get_filter_stats method exists."""
        assert hasattr(movie_manager, 'get_filter_stats')


if __name__ == "__main__":
    pytest.main([__file__]) 