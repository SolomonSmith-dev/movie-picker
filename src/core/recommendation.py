"""Simple content-based recommendation engine for MoviePicker."""

import random
from typing import List, Dict
from collections import Counter
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .models import Movie, WatchHistory, UserRating
from .database import db_manager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationEngine:
    """Simple content-based movie recommendation engine."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def get_user_preferences(self, user_id: int = 1) -> Dict:
        """Extract user preferences from watch history and ratings."""
        preferences = {
            "favorite_genres": [],
            "favorite_directors": [],
            "favorite_actors": [],
            "preferred_years": [],
            "min_rating": 0,
            "excluded_genres": [],
        }

        with db_manager.get_session() as session:
            # Get highly rated movies (rating >= 7)
            high_rated = (
                session.query(UserRating)
                .filter(and_(UserRating.user_id == user_id, UserRating.rating >= 7))
                .all()
            )

            # Get favorite movies
            favorites = (
                session.query(WatchHistory)
                .filter(
                    and_(
                        WatchHistory.user_id == user_id,
                        WatchHistory.is_favorite.is_(True),
                    )
                )
                .all()
            )

            # Combine high-rated and favorite movies
            liked_movies = []
            for rating in high_rated:
                movie = session.query(Movie).filter(Movie.id == rating.movie_id).first()
                if movie:
                    liked_movies.append(movie)

            for fav in favorites:
                movie = session.query(Movie).filter(Movie.id == fav.movie_id).first()
                if movie and movie not in liked_movies:
                    liked_movies.append(movie)

            # Extract preferences from liked movies
            genres = []
            directors = []
            actors = []
            years = []

            for movie in liked_movies:
                if movie.genres:
                    genres.extend([g.strip() for g in movie.genres.split(",")])
                if movie.director:
                    directors.append(movie.director)
                if movie.cast:
                    actors.extend([a.strip() for a in movie.cast.split(",")])
                if movie.year:
                    years.append(movie.year)

            # Get most common preferences
            if genres:
                genre_counter = Counter(genres)
                preferences["favorite_genres"] = [
                    genre for genre, count in genre_counter.most_common(5)
                ]

            if directors:
                director_counter = Counter(directors)
                preferences["favorite_directors"] = [
                    director for director, count in director_counter.most_common(3)
                ]

            if actors:
                actor_counter = Counter(actors)
                preferences["favorite_actors"] = [
                    actor for actor, count in actor_counter.most_common(5)
                ]

            if years:
                # Get preferred year range (most common years ± 5 years)
                year_counter = Counter(years)
                most_common_year = year_counter.most_common(1)[0][0]
                preferences["preferred_years"] = list(
                    range(most_common_year - 5, most_common_year + 6)
                )

            # Get minimum rating preference
            if high_rated:
                avg_rating = sum(r.rating for r in high_rated) / len(high_rated)
                preferences["min_rating"] = max(
                    0, avg_rating - 2
                )  # Suggest movies rated within 2 points of average

        return preferences

    def get_recommendations(
        self,
        user_id: int = 1,
        limit: int = 10,
        exclude_watched: bool = True,
        surprise_me: bool = False,
    ) -> List[Movie]:
        """Get movie recommendations for a user."""

        if surprise_me:
            return self._get_surprise_recommendations(user_id, limit, exclude_watched)

        preferences = self.get_user_preferences(user_id)

        with db_manager.get_session() as session:
            # Build query for recommendations
            query = session.query(Movie)

            # Exclude watched movies if requested
            if exclude_watched:
                watched_movies = (
                    session.query(WatchHistory)
                    .filter(WatchHistory.user_id == user_id)
                    .all()
                )
                watched_ids = [wh.movie_id for wh in watched_movies]
                if watched_ids:
                    query = query.filter(~Movie.id.in_(watched_ids))

            # Apply preference filters
            filters = []

            # Genre filter
            if preferences["favorite_genres"]:
                genre_filters = []
                for genre in preferences["favorite_genres"][:3]:  # Top 3 genres
                    genre_filters.append(Movie.genres.ilike(f"%{genre}%"))
                if genre_filters:
                    filters.append(or_(*genre_filters))

            # Director filter
            if preferences["favorite_directors"]:
                director_filters = []
                for director in preferences["favorite_directors"]:
                    director_filters.append(Movie.director.ilike(f"%{director}%"))
                if director_filters:
                    filters.append(or_(*director_filters))

            # Actor filter
            if preferences["favorite_actors"]:
                actor_filters = []
                for actor in preferences["favorite_actors"][:3]:  # Top 3 actors
                    actor_filters.append(Movie.cast.ilike(f"%{actor}%"))
                if actor_filters:
                    filters.append(or_(*actor_filters))

            # Year filter
            if preferences["preferred_years"]:
                filters.append(Movie.year.in_(preferences["preferred_years"]))

            # Rating filter
            if preferences["min_rating"] > 0:
                filters.append(Movie.rating >= preferences["min_rating"])

            # Apply all filters
            if filters:
                query = query.filter(or_(*filters))

            # Order by rating (descending) and limit results
            recommendations = (
                query.order_by(Movie.rating.desc().nullslast()).limit(limit * 2).all()
            )

            # If we don't have enough recommendations, add some random ones
            if len(recommendations) < limit:
                remaining = limit - len(recommendations)
                additional = self._get_random_movies(
                    session, remaining, exclude_watched, user_id
                )
                recommendations.extend(additional)

            # Shuffle and return top results
            random.shuffle(recommendations)
            result = recommendations[:limit]

            # Create new Movie objects to avoid session issues
            detached_movies = []
            for movie in result:
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
                    country=movie.country,
                )
                detached_movies.append(detached_movie)

            return detached_movies

    def _get_surprise_recommendations(
        self, user_id: int, limit: int, exclude_watched: bool
    ) -> List[Movie]:
        """Get completely random movie recommendations."""
        with db_manager.get_session() as session:
            movies = self._get_random_movies(session, limit, exclude_watched, user_id)

            # Create new Movie objects to avoid session issues
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
                    country=movie.country,
                )
                detached_movies.append(detached_movie)

            return detached_movies

    def _get_random_movies(
        self, session: Session, limit: int, exclude_watched: bool, user_id: int
    ) -> List[Movie]:
        """Get random movies, optionally excluding watched ones."""
        query = session.query(Movie)

        if exclude_watched:
            watched_movies = (
                session.query(WatchHistory)
                .filter(WatchHistory.user_id == user_id)
                .all()
            )
            watched_ids = [wh.movie_id for wh in watched_movies]
            if watched_ids:
                query = query.filter(~Movie.id.in_(watched_ids))

        # Get all movies and shuffle
        all_movies = query.all()
        random.shuffle(all_movies)

        return all_movies[:limit]

    def get_similar_movies(self, movie_id: int, limit: int = 5) -> List[Movie]:
        """Get movies similar to a specific movie."""
        with db_manager.get_session() as session:
            target_movie = session.query(Movie).filter(Movie.id == movie_id).first()
            if not target_movie:
                return []

            # Find movies with similar attributes
            similar_movies = []

            # Same director
            if target_movie.director:
                director_movies = (
                    session.query(Movie)
                    .filter(
                        and_(
                            Movie.director == target_movie.director,
                            Movie.id != movie_id,
                        )
                    )
                    .limit(limit)
                    .all()
                )
                similar_movies.extend(director_movies)

            # Same genres
            if target_movie.genres:
                genre_list = [g.strip() for g in target_movie.genres.split(",")]
                for genre in genre_list[:2]:  # Top 2 genres
                    genre_movies = (
                        session.query(Movie)
                        .filter(
                            and_(Movie.genres.ilike(f"%{genre}%"), Movie.id != movie_id)
                        )
                        .limit(limit)
                        .all()
                    )
                    similar_movies.extend(genre_movies)

            # Same year range (± 2 years)
            if target_movie.year:
                year_range = range(target_movie.year - 2, target_movie.year + 3)
                year_movies = (
                    session.query(Movie)
                    .filter(and_(Movie.year.in_(year_range), Movie.id != movie_id))
                    .limit(limit)
                    .all()
                )
                similar_movies.extend(year_movies)

            # Remove duplicates and limit results
            seen_ids = set()
            unique_movies = []
            for movie in similar_movies:
                if movie.id not in seen_ids:
                    seen_ids.add(movie.id)
                    unique_movies.append(movie)
                    if len(unique_movies) >= limit:
                        break

            # Create new Movie objects to avoid session issues
            detached_movies = []
            for movie in unique_movies:
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
                    country=movie.country,
                )
                detached_movies.append(detached_movie)

            return detached_movies


# Global recommendation engine instance
recommendation_engine = RecommendationEngine()
