"""Pytest configuration and fixtures for MoviePicker tests."""

import pytest
import tempfile
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

from src.core.models import Base, Movie, User, WatchHistory, UserRating
from src.core.database import db_manager
from src.core.movie_manager import MovieManager


@pytest.fixture
def test_database_url():
    """Create a unique in-memory SQLite database for each test."""
    import uuid
    # Use a unique database name for each test to ensure complete isolation
    return f"sqlite:///:memory:?cache=shared&uri=true&id={uuid.uuid4().hex}"


@pytest.fixture
def test_engine(test_database_url):
    """Create a test database engine for each test."""
    engine = create_engine(test_database_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    # Clean up
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_session_factory(test_engine):
    """Create a session factory for test database."""
    return sessionmaker(bind=test_engine)


@pytest.fixture
def test_db_session(test_engine, test_session_factory):
    """Create a database session for a test, with proper cleanup."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = test_session_factory(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def mock_db_manager(test_db_session):
    """Mock the db_manager to use test database session."""
    with patch('src.core.movie_manager.db_manager') as mock_manager1, \
         patch('src.core.filters.db_manager') as mock_manager2:
        # Create a context manager that returns our test session for both imports
        for mock_manager in [mock_manager1, mock_manager2]:
            mock_manager.get_session.return_value.__enter__.return_value = test_db_session
            mock_manager.get_session.return_value.__exit__.return_value = None
        yield mock_manager1


@pytest.fixture
def sample_movies():
    """Create sample movie data for testing."""
    return [
        Movie(
            title="The Matrix",
            director="The Wachowskis",
            year=1999,
            genres="Action, Sci-Fi",
            cast="Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
            rating=8.7,
            runtime=136,
            language="en",
            country="US",
            overview="A hacker discovers the reality he knows is a simulation."
        ),
        Movie(
            title="Pulp Fiction",
            director="Quentin Tarantino",
            year=1994,
            genres="Crime, Drama",
            cast="John Travolta, Uma Thurman, Samuel L. Jackson",
            rating=8.9,
            runtime=154,
            language="en",
            country="US",
            overview="The lives of two mob hitmen intertwine in four tales of violence and redemption."
        ),
        Movie(
            title="The Dark Knight",
            director="Christopher Nolan",
            year=2008,
            genres="Action, Crime, Drama",
            cast="Christian Bale, Heath Ledger, Aaron Eckhart",
            rating=9.0,
            runtime=152,
            language="en",
            country="US",
            overview="Batman faces the Joker, a criminal mastermind who wants to watch the world burn."
        ),
        Movie(
            title="Parasite",
            director="Bong Joon-ho",
            year=2023,  # Updated to recent year for testing
            genres="Comedy, Drama, Thriller",
            cast="Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
            rating=8.6,
            runtime=132,
            language="ko",
            country="KR",
            overview="A poor family schemes to become employed by a wealthy family."
        ),
        Movie(
            title="Inception",
            director="Christopher Nolan",
            year=2022,  # Updated to recent year for testing
            genres="Action, Sci-Fi, Thriller",
            cast="Leonardo DiCaprio, Marion Cotillard, Tom Hardy",
            rating=8.8,
            runtime=148,
            language="en",
            country="US",
            overview="A thief who steals corporate secrets through dream-sharing technology."
        )
    ]


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    return User(
        username=f"testuser_{unique_id}",
        email=f"test_{unique_id}@example.com",
        preferences='{"genres": ["Action", "Sci-Fi"], "min_rating": 7.0}'
    )


@pytest.fixture
def populated_test_db(test_db_session, sample_movies, sample_user):
    """Create a test database populated with sample data."""
    # Add user
    test_db_session.add(sample_user)
    test_db_session.flush()  # Get the user ID
    
    # Add movies
    for movie in sample_movies:
        test_db_session.add(movie)
    test_db_session.flush()  # Get the movie IDs
    
    # Add some watch history - use the actual generated IDs
    user_id = sample_user.id
    movie1_id = sample_movies[0].id  # The Matrix
    movie2_id = sample_movies[1].id  # Pulp Fiction
    
    watch_history_entries = [
        WatchHistory(user_id=user_id, movie_id=movie1_id, is_favorite=True),
        WatchHistory(user_id=user_id, movie_id=movie2_id, is_favorite=False),
    ]
    for entry in watch_history_entries:
        test_db_session.add(entry)
    
    # Add some ratings
    ratings = [
        UserRating(user_id=user_id, movie_id=movie1_id, rating=9, review="Excellent movie!"),
        UserRating(user_id=user_id, movie_id=movie2_id, rating=8, review="Great storytelling."),
    ]
    for rating in ratings:
        test_db_session.add(rating)
    
    test_db_session.commit()
    return test_db_session


@pytest.fixture
def movie_manager_with_test_db(mock_db_manager):
    """Create a MovieManager instance using the test database."""
    return MovieManager()


@pytest.fixture
def mock_tmdb_client():
    """Mock TMDb client to avoid real API calls during testing."""
    with patch('src.api.tmdb_client.TMDbClient') as mock_client:
        # Configure mock responses
        mock_instance = mock_client.return_value
        mock_instance.search_movies.return_value = [
            {
                'id': 123,
                'title': 'Test Movie',
                'overview': 'A test movie',
                'release_date': '2023-01-01',
                'vote_average': 8.0,
                'poster_path': '/test_poster.jpg'
            }
        ]
        mock_instance.get_movie_details.return_value = {
            'id': 123,
            'title': 'Test Movie',
            'overview': 'A test movie',
            'release_date': '2023-01-01',
            'vote_average': 8.0,
            'runtime': 120,
            'genres': [{'name': 'Action'}, {'name': 'Adventure'}],
            'credits': {
                'cast': [
                    {'name': 'Test Actor 1'},
                    {'name': 'Test Actor 2'}
                ],
                'crew': [
                    {'job': 'Director', 'name': 'Test Director'}
                ]
            }
        }
        yield mock_instance


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables and configurations."""
    # Set test environment variables
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['LOG_LEVEL'] = 'WARNING'  # Reduce log noise during tests
    
    # Create temporary directories for test data if needed
    test_data_dir = Path(tempfile.mkdtemp(prefix="moviepicker_test_"))
    os.environ['TEST_DATA_DIR'] = str(test_data_dir)
    
    yield
    
    # Cleanup
    if 'TEST_DATA_DIR' in os.environ:
        del os.environ['TEST_DATA_DIR']
    if 'ENVIRONMENT' in os.environ:
        del os.environ['ENVIRONMENT']


# Test markers for different test types
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require external dependencies"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that require database or external services"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )
    config.addinivalue_line(
        "markers", "tmdb: Tests that require TMDb API (mocked or real)"
    )