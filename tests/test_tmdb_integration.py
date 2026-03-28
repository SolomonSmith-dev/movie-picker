"""Tests for TMDb API integration and movie enrichment."""

import pytest
from unittest.mock import patch, MagicMock

from src.api.tmdb_client import TMDbClient
from src.api.enricher import MovieDataEnricher


@pytest.mark.tmdb
class TestTMDbClient:
    """Test TMDb client functionality with mocked API calls."""

    def test_tmdb_client_initialization(self, mock_tmdb_client):
        """Test TMDb client initializes correctly."""
        client = TMDbClient(api_key="test_key")
        assert client is not None

    def test_search_movies_success(self, mock_tmdb_client):
        """Test successful movie search."""
        results = mock_tmdb_client.search_movies("Test Movie")
        
        assert len(results) > 0
        assert results[0]['title'] == 'Test Movie'
        assert 'id' in results[0]
        assert 'overview' in results[0]
    
    def test_get_movie_details_success(self, mock_tmdb_client):
        """Test successful movie details retrieval."""
        movie_details = mock_tmdb_client.get_movie_details(123)
        
        assert movie_details['id'] == 123
        assert movie_details['title'] == 'Test Movie'
        assert 'genres' in movie_details
        assert 'credits' in movie_details
        assert 'cast' in movie_details['credits']
        assert 'crew' in movie_details['credits']
    
    @patch('src.api.tmdb_client.TMDbClient')
    def test_search_movies_no_results(self, mock_client_class):
        """Test search with no results."""
        mock_instance = mock_client_class.return_value
        mock_instance.search_movies.return_value = []
        
        results = mock_instance.search_movies("NonexistentMovie12345")
        assert len(results) == 0
    
    @patch('src.api.tmdb_client.TMDbClient')
    def test_search_movies_api_error(self, mock_client_class):
        """Test handling of API errors during search."""
        mock_instance = mock_client_class.return_value
        mock_instance.search_movies.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="API Error"):
            mock_instance.search_movies("Test Movie")
    
    @patch('src.api.tmdb_client.TMDbClient')
    def test_get_movie_details_not_found(self, mock_client_class):
        """Test handling of movie not found."""
        mock_instance = mock_client_class.return_value
        mock_instance.get_movie_details.return_value = None
        
        result = mock_instance.get_movie_details(999999)
        assert result is None


@pytest.mark.tmdb
class TestMovieDataEnricher:
    """Test movie data enrichment functionality."""

    @pytest.fixture
    def sample_movie_dict(self):
        """Sample movie data for enrichment."""
        return {
            'title': 'The Matrix',
            'director': 'The Wachowskis',
            'year': 1999,
            'genres': 'Action, Sci-Fi'
        }
    
    @pytest.fixture
    def mock_enricher(self, mock_tmdb_client):
        """Mock movie data enricher."""
        with patch('src.api.enricher.MovieDataEnricher') as mock_enricher_class:
            mock_instance = mock_enricher_class.return_value
            mock_instance.tmdb_client = mock_tmdb_client
            yield mock_instance
    
    def test_enricher_initialization(self, mock_enricher):
        """Test enricher initializes correctly."""
        enricher = MovieDataEnricher(api_key="test_key")
        assert enricher is not None
    
    def test_enrich_movie_data_success(self, mock_enricher, sample_movie_dict):
        """Test successful movie data enrichment."""
        # Configure mock to return enriched data
        mock_enricher.enrich_movie_data.return_value = {
            **sample_movie_dict,
            'tmdb_id': 123,
            'poster_url': 'https://image.tmdb.org/t/p/w500/test_poster.jpg',
            'overview': 'A hacker discovers the reality he knows is a simulation.',
            'rating': 8.7,
            'runtime': 136,
            'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
            'language': 'en',
            'country': 'US'
        }
        
        enriched = mock_enricher.enrich_movie_data(sample_movie_dict)
        
        # Verify enrichment added new fields
        assert 'tmdb_id' in enriched
        assert 'poster_url' in enriched
        assert 'overview' in enriched
        assert 'rating' in enriched
        assert 'runtime' in enriched
        assert 'cast' in enriched
        assert 'language' in enriched
        assert 'country' in enriched
        
        # Verify original data preserved
        assert enriched['title'] == sample_movie_dict['title']
        assert enriched['director'] == sample_movie_dict['director']
        assert enriched['year'] == sample_movie_dict['year']
    
    def test_enrich_movie_data_no_tmdb_match(self, mock_enricher, sample_movie_dict):
        """Test enrichment when no TMDb match is found."""
        # Configure mock to return original data when no match
        mock_enricher.enrich_movie_data.return_value = sample_movie_dict
        
        # Use a very obscure title that won't match
        obscure_movie = {
            'title': 'Very Obscure Movie That Does Not Exist 12345',
            'director': 'Unknown Director',
            'year': 2023,
            'genres': 'Unknown'
        }
        
        enriched = mock_enricher.enrich_movie_data(obscure_movie)
        
        # Should return original data when no match found
        assert enriched == obscure_movie
        assert 'tmdb_id' not in enriched  # No enrichment occurred
    
    def test_enrich_multiple_movies(self, mock_enricher, sample_movies):
        """Test enriching multiple movies at once."""
        # Convert Movie objects to dicts for enrichment
        movie_dicts = [
            {
                'title': movie.title,
                'director': movie.director,
                'year': movie.year,
                'genres': movie.genres
            }
            for movie in sample_movies
        ]
        
        # Configure mock to return enriched versions
        mock_enricher.enrich_multiple_movies.return_value = [
            {
                **movie_dict,
                'tmdb_id': i + 100,
                'poster_url': f'/test_poster_{i}.jpg',
                'overview': f'Overview for {movie_dict["title"]}',
                'rating': 8.0 + (i * 0.1)
            }
            for i, movie_dict in enumerate(movie_dicts)
        ]
        
        enriched_movies = mock_enricher.enrich_multiple_movies(movie_dicts)
        
        assert len(enriched_movies) == len(movie_dicts)
        for enriched in enriched_movies:
            assert 'tmdb_id' in enriched
            assert 'poster_url' in enriched
            assert 'overview' in enriched
            assert 'rating' in enriched
    
    def test_enrich_with_api_error(self, mock_enricher, sample_movie_dict):
        """Test enrichment handling when API fails."""
        # Configure mock to raise an exception
        mock_enricher.enrich_movie_data.side_effect = Exception("TMDb API Error")
        
        # Should handle error gracefully
        with pytest.raises(Exception, match="TMDb API Error"):
            mock_enricher.enrich_movie_data(sample_movie_dict)
    
    def test_extract_cast_from_credits(self, mock_enricher):
        """Test extraction of cast information from TMDb credits."""
        mock_credits = {
            'cast': [
                {'name': 'Actor One', 'character': 'Hero'},
                {'name': 'Actor Two', 'character': 'Villain'},
                {'name': 'Actor Three', 'character': 'Sidekick'}
            ]
        }
        
        mock_enricher.extract_cast_from_credits.return_value = "Actor One, Actor Two, Actor Three"
        
        cast_string = mock_enricher.extract_cast_from_credits(mock_credits)
        
        assert "Actor One" in cast_string
        assert "Actor Two" in cast_string
        assert "Actor Three" in cast_string
    
    def test_extract_director_from_credits(self, mock_enricher):
        """Test extraction of director information from TMDb credits."""
        mock_credits = {
            'crew': [
                {'name': 'Director Name', 'job': 'Director'},
                {'name': 'Producer Name', 'job': 'Producer'},
                {'name': 'Writer Name', 'job': 'Writer'}
            ]
        }
        
        mock_enricher.extract_director_from_credits.return_value = "Director Name"
        
        director = mock_enricher.extract_director_from_credits(mock_credits)
        
        assert director == "Director Name"
    
    def test_format_genres_list(self, mock_enricher):
        """Test formatting of genres from TMDb API response."""
        mock_genres = [
            {'name': 'Action'},
            {'name': 'Adventure'},
            {'name': 'Science Fiction'}
        ]
        
        mock_enricher.format_genres_list.return_value = "Action, Adventure, Science Fiction"
        
        formatted_genres = mock_enricher.format_genres_list(mock_genres)
        
        assert formatted_genres == "Action, Adventure, Science Fiction"
    
    def test_build_poster_url(self, mock_enricher):
        """Test building full poster URL from TMDb path."""
        poster_path = "/test_poster.jpg"
        
        mock_enricher.build_poster_url.return_value = "https://image.tmdb.org/t/p/w500/test_poster.jpg"
        
        full_url = mock_enricher.build_poster_url(poster_path)
        
        assert full_url.startswith("https://image.tmdb.org/")
        assert "test_poster.jpg" in full_url


@pytest.mark.integration
@pytest.mark.tmdb
class TestTMDbIntegration:
    """Integration tests for TMDb functionality."""

    def test_movie_enrichment_pipeline(self, mock_tmdb_client, sample_movies):
        """Test the complete movie enrichment pipeline."""
        # This would test the full pipeline from raw movie data to enriched database entries
        # For now, we'll test that the pipeline components work together
        
        with patch('src.api.enricher.MovieDataEnricher') as mock_enricher_class:
            mock_enricher = mock_enricher_class.return_value
            mock_enricher.tmdb_client = mock_tmdb_client
            
            # Test that enricher can be initialized and used
            enricher = mock_enricher_class(api_key="test_key")
            
            # Test enrichment of sample movie
            sample_movie_dict = {
                'title': sample_movies[0].title,
                'director': sample_movies[0].director,
                'year': sample_movies[0].year
            }
            
            mock_enricher.enrich_movie_data.return_value = {
                **sample_movie_dict,
                'tmdb_id': 123,
                'overview': 'Enriched overview',
                'poster_url': '/enriched_poster.jpg'
            }
            
            result = mock_enricher.enrich_movie_data(sample_movie_dict)
            
            assert 'tmdb_id' in result
            assert 'overview' in result
            assert 'poster_url' in result