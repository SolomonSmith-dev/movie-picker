"""Advanced filtering system for MoviePicker application."""

from typing import List, Dict, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, between, func

from .models import Movie, WatchHistory
from .database import db_manager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MovieFilter:
    """Advanced movie filtering system."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def filter_movies(
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
        """Filter movies based on multiple criteria."""
        
        with db_manager.get_session() as session:
            query = session.query(Movie)
            
            # Year range filter
            if year_min is not None or year_max is not None:
                if year_min is not None and year_max is not None:
                    query = query.filter(Movie.year.between(year_min, year_max))
                elif year_min is not None:
                    query = query.filter(Movie.year >= year_min)
                elif year_max is not None:
                    query = query.filter(Movie.year <= year_max)
            
            # Rating range filter
            if rating_min is not None or rating_max is not None:
                if rating_min is not None and rating_max is not None:
                    query = query.filter(Movie.rating.between(rating_min, rating_max))
                elif rating_min is not None:
                    query = query.filter(Movie.rating >= rating_min)
                elif rating_max is not None:
                    query = query.filter(Movie.rating <= rating_max)
            
            # Runtime range filter
            if runtime_min is not None or runtime_max is not None:
                if runtime_min is not None and runtime_max is not None:
                    query = query.filter(Movie.runtime.between(runtime_min, runtime_max))
                elif runtime_min is not None:
                    query = query.filter(Movie.runtime >= runtime_min)
                elif runtime_max is not None:
                    query = query.filter(Movie.runtime <= runtime_max)
            
            # Genre filter
            if genres:
                genre_filters = []
                for genre in genres:
                    genre_filters.append(Movie.genres.ilike(f"%{genre}%"))
                if genre_filters:
                    query = query.filter(or_(*genre_filters))
            
            # Director filter
            if directors:
                director_filters = []
                for director in directors:
                    director_filters.append(Movie.director.ilike(f"%{director}%"))
                if director_filters:
                    query = query.filter(or_(*director_filters))
            
            # Actor filter
            if actors:
                actor_filters = []
                for actor in actors:
                    actor_filters.append(Movie.cast.ilike(f"%{actor}%"))
                if actor_filters:
                    query = query.filter(or_(*actor_filters))
            
            # Language filter
            if languages:
                query = query.filter(Movie.language.in_(languages))
            
            # Country filter
            if countries:
                country_filters = []
                for country in countries:
                    country_filters.append(Movie.country.ilike(f"%{country}%"))
                if country_filters:
                    query = query.filter(or_(*country_filters))
            
            # Exclude watched movies
            if exclude_watched:
                watched_movies = session.query(WatchHistory).filter(
                    WatchHistory.user_id == user_id
                ).all()
                watched_ids = [wh.movie_id for wh in watched_movies]
                if watched_ids:
                    query = query.filter(~Movie.id.in_(watched_ids))
            
            # Ordering
            if order_by == "rating":
                if order_direction == "desc":
                    query = query.order_by(Movie.rating.desc().nullslast())
                else:
                    query = query.order_by(Movie.rating.asc().nullslast())
            elif order_by == "year":
                if order_direction == "desc":
                    query = query.order_by(Movie.year.desc().nullslast())
                else:
                    query = query.order_by(Movie.year.asc().nullslast())
            elif order_by == "title":
                if order_direction == "desc":
                    query = query.order_by(Movie.title.desc())
                else:
                    query = query.order_by(Movie.title.asc())
            elif order_by == "runtime":
                if order_direction == "desc":
                    query = query.order_by(Movie.runtime.desc().nullslast())
                else:
                    query = query.order_by(Movie.runtime.asc().nullslast())
            
            # Limit results
            if limit:
                query = query.limit(limit)
            
            movies = query.all()
            
            # Create detached Movie objects to avoid session issues
            detached_movies = []
            for movie in movies:
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
                detached_movies.append(detached_movie)
            
            return detached_movies
    
    def get_filter_stats(self) -> Dict:
        """Get statistics about available movies for filtering."""
        with db_manager.get_session() as session:
            stats = {}
            
            # Year range
            year_stats = session.query(
                func.min(Movie.year).label('min_year'),
                func.max(Movie.year).label('max_year')
            ).first()
            stats['year_range'] = {
                'min': year_stats.min_year,
                'max': year_stats.max_year
            }
            
            # Rating range
            rating_stats = session.query(
                func.min(Movie.rating).label('min_rating'),
                func.max(Movie.rating).label('max_rating'),
                func.avg(Movie.rating).label('avg_rating')
            ).first()
            stats['rating_range'] = {
                'min': rating_stats.min_rating or 0.0,
                'max': rating_stats.max_rating or 0.0,
                'average': rating_stats.avg_rating or 0.0
            }
            
            # Runtime range
            runtime_stats = session.query(
                func.min(Movie.runtime).label('min_runtime'),
                func.max(Movie.runtime).label('max_runtime'),
                func.avg(Movie.runtime).label('avg_runtime')
            ).first()
            stats['runtime_range'] = {
                'min': runtime_stats.min_runtime or 0,
                'max': runtime_stats.max_runtime or 0,
                'average': runtime_stats.avg_runtime or 0
            }
            
            # Available genres
            all_genres = session.query(Movie.genres).filter(Movie.genres.isnot(None)).all()
            genre_set = set()
            for movie_genres in all_genres:
                if movie_genres.genres:
                    genres = [g.strip() for g in movie_genres.genres.split(',')]
                    genre_set.update(genres)
            stats['available_genres'] = sorted(list(genre_set))
            
            # Available languages
            languages = session.query(Movie.language).filter(
                Movie.language.isnot(None)
            ).distinct().all()
            stats['available_languages'] = [lang.language for lang in languages if lang.language]
            
            # Total movie count
            stats['total_movies'] = session.query(Movie).count()
            
            return stats
    
    def fuzzy_search(self, query: str, limit: int = 20) -> List[Movie]:
        """Fuzzy search across title, director, cast, and overview."""
        with db_manager.get_session() as session:
            search_query = session.query(Movie).filter(
                or_(
                    Movie.title.ilike(f"%{query}%"),
                    Movie.director.ilike(f"%{query}%"),
                    Movie.cast.ilike(f"%{query}%"),
                    Movie.overview.ilike(f"%{query}%")
                )
            ).limit(limit).all()
            
            # Create detached Movie objects
            detached_movies = []
            for movie in search_query:
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
                detached_movies.append(detached_movie)
            
            return detached_movies


# Global filter instance
movie_filter = MovieFilter() 