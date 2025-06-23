"""Movie management and operations for MoviePicker application."""

import random
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import Movie, WatchHistory, User, UserRating
from .database import db_manager
from .recommendation import RecommendationEngine
from .filters import movie_filter
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MovieManager:
    """Manages movie operations and data access."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.recommendation_engine = RecommendationEngine()
    
    def get_movie_of_the_day(self) -> Optional[Movie]:
        """Get a random movie for the day."""
        with db_manager.get_session() as session:
            # Use date as seed for consistent daily selection
            today = datetime.now().strftime("%Y-%m-%d")
            random.seed(today)
            
            movies = session.query(Movie).all()
            if not movies:
                return None
            
            movie = random.choice(movies)
            
            # Create detached Movie object
            detached_movie = Movie(
                id=movie.id,
                title=movie.title,
                director=movie.director,
                year=movie.year,
                genres=movie.genres,
                cast=movie.cast,
                tmdb_id=movie.tmdb_id,
                poster_url=movie.poster_url,
                overview=movie.overview,
                rating=movie.rating,
                runtime=movie.runtime,
                language=movie.language,
                country=movie.country
            )
            
            return detached_movie
    
    def get_movies_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        """Get movies by genre."""
        return movie_filter.filter_movies(genres=[genre], limit=limit)
    
    def get_top_rated_movies(self, limit: int = 10) -> List[Movie]:
        """Get top rated movies."""
        return movie_filter.filter_movies(
            rating_min=7.0,
            order_by="rating",
            order_direction="desc",
            limit=limit
        )
    
    def get_recent_movies(self, limit: int = 10) -> List[Movie]:
        """Get recent movies (last 5 years)."""
        current_year = datetime.now().year
        return movie_filter.filter_movies(
            year_min=current_year - 5,
            order_by="year",
            order_direction="desc",
            limit=limit
        )
    
    def search_movies(self, query: str, limit: int = 20) -> List[Movie]:
        """Search movies by title, director, or cast."""
        return movie_filter.fuzzy_search(query, limit)
    
    def get_watch_history(self, user_id: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's watch history."""
        with db_manager.get_session() as session:
            history = session.query(WatchHistory).filter(
                WatchHistory.user_id == user_id
            ).order_by(WatchHistory.watched_at.desc()).limit(limit).all()
            
            result = []
            for entry in history:
                movie = session.query(Movie).filter(Movie.id == entry.movie_id).first()
                if movie:
                    # Get user rating if it exists
                    user_rating = session.query(UserRating).filter(
                        UserRating.user_id == user_id,
                        UserRating.movie_id == entry.movie_id
                    ).first()
                    
                    result.append({
                        'movie': {
                            'id': movie.id,
                            'title': movie.title,
                            'director': movie.director,
                            'year': movie.year,
                            'genres': movie.genres,
                            'rating': movie.rating,
                            'poster_url': movie.poster_url
                        },
                        'watched_at': entry.watched_at,
                        'rating': user_rating.rating if user_rating else None
                    })
            
            return result
    
    def mark_as_watched(self, movie_id: int, user_id: int = 1, rating: Optional[float] = None) -> bool:
        """Mark a movie as watched."""
        try:
            with db_manager.get_session() as session:
                # Check if already watched
                existing = session.query(WatchHistory).filter(
                    WatchHistory.movie_id == movie_id,
                    WatchHistory.user_id == user_id
                ).first()
                
                if existing:
                    # Update existing entry
                    existing.watched_at = datetime.now()
                else:
                    # Create new watch history entry
                    watch_history = WatchHistory(
                        movie_id=movie_id,
                        user_id=user_id,
                        watched_at=datetime.now()
                    )
                    session.add(watch_history)
                
                # Handle rating
                if rating is not None:
                    # Check if user already rated this movie
                    existing_rating = session.query(UserRating).filter(
                        UserRating.movie_id == movie_id,
                        UserRating.user_id == user_id
                    ).first()
                    
                    if existing_rating:
                        # Update existing rating
                        existing_rating.rating = int(rating)
                        existing_rating.rated_at = datetime.now()
                    else:
                        # Create new rating
                        user_rating = UserRating(
                            movie_id=movie_id,
                            user_id=user_id,
                            rating=int(rating),
                            rated_at=datetime.now()
                        )
                        session.add(user_rating)
                
                session.commit()
                logger.info(f"Marked movie {movie_id} as watched for user {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error marking movie as watched: {e}")
            return False
    
    def get_recommendations(self, user_id: int = 1, limit: int = 10) -> Dict[str, List[Movie]]:
        """Get personalized movie recommendations."""
        recommendations = self.recommendation_engine.get_recommendations(user_id, limit)
        
        # The recommendation engine returns a List[Movie], but we need to return a Dict
        # For now, we'll categorize them as "Personalized" recommendations
        return {
            "Personalized": recommendations
        }
    
    def get_filter_stats(self) -> Dict:
        """Get statistics for filtering."""
        return movie_filter.get_filter_stats()
    
    def advanced_filter(
        self,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        rating_min: Optional[float] = None,
        rating_max: Optional[float] = None,
        runtime_min: Optional[int] = None,
        runtime_max: Optional[int] = None,
        genres: Optional[List[str]] = None,
        directors: Optional[List[str]] = None,
        actors: Optional[List[str]] = None,
        languages: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        exclude_watched: bool = False,
        user_id: int = 1,
        limit: Optional[int] = None,
        order_by: str = "rating",
        order_direction: str = "desc"
    ) -> List[Movie]:
        """Advanced movie filtering with multiple criteria."""
        return movie_filter.filter_movies(
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
            user_id=user_id,
            limit=limit,
            order_by=order_by,
            order_direction=order_direction
        )


# Global movie manager instance
movie_manager = MovieManager() 