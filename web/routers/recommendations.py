"""Recommendations API router for MoviePicker."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

# Add src to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.movie_manager import movie_manager
from src.core.models import Movie

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class MovieResponse(BaseModel):
    """Movie response model."""
    id: int
    title: str
    director: Optional[str] = None
    year: Optional[int] = None
    genres: Optional[str] = None
    cast: Optional[str] = None
    tmdb_id: Optional[int] = None
    poster_url: Optional[str] = None
    overview: Optional[str] = None
    rating: Optional[float] = None
    runtime: Optional[int] = None
    language: Optional[str] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    """Recommendation response model."""
    category: str
    movies: List[MovieResponse]
    reason: str


class RecommendationsResponse(BaseModel):
    """Full recommendations response model."""
    user_id: int
    recommendations: List[RecommendationResponse]
    total_recommendations: int


@router.get("/{user_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations per category")
):
    """Get personalized recommendations for a user."""
    try:
        recommendations = movie_manager.get_recommendations(user_id=user_id, limit=limit)
        
        # Convert to response format
        recommendation_responses = []
        total_count = 0
        
        for category, movies in recommendations.items():
            if movies:
                movie_responses = [MovieResponse.from_orm(movie) for movie in movies]
                recommendation_responses.append(RecommendationResponse(
                    category=category,
                    movies=movie_responses,
                    reason=f"Based on your {category.lower()} preferences"
                ))
                total_count += len(movie_responses)
        
        return RecommendationsResponse(
            user_id=user_id,
            recommendations=recommendation_responses,
            total_recommendations=total_count
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")


@router.get("/{user_id}/personalized", response_model=List[MovieResponse])
async def get_personalized_recommendations(
    user_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations to return")
):
    """Get personalized recommendations (flattened list)."""
    try:
        recommendations = movie_manager.get_recommendations(user_id=user_id, limit=limit)
        
        # Flatten all recommendations into a single list
        all_movies = []
        for movies in recommendations.values():
            all_movies.extend(movies)
        
        # Return up to the requested limit
        return [MovieResponse.from_orm(movie) for movie in all_movies[:limit]]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching personalized recommendations: {str(e)}")


@router.get("/{user_id}/surprise", response_model=MovieResponse)
async def get_surprise_recommendation(user_id: int):
    """Get a surprise recommendation for a user."""
    try:
        recommendations = movie_manager.get_recommendations(user_id=user_id, limit=20)
        
        # Get all movies from all categories
        all_movies = []
        for movies in recommendations.values():
            all_movies.extend(movies)
        
        if not all_movies:
            raise HTTPException(status_code=404, detail="No recommendations available")
        
        # Pick a random movie
        import random
        surprise_movie = random.choice(all_movies)
        
        return MovieResponse.from_orm(surprise_movie)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching surprise recommendation: {str(e)}")


@router.get("/{user_id}/similar/{movie_id}", response_model=List[MovieResponse])
async def get_similar_movies(
    user_id: int,
    movie_id: int,
    limit: int = Query(5, ge=1, le=20, description="Number of similar movies to return")
):
    """Get movies similar to a specific movie."""
    try:
        # TODO: Implement similar movies in movie_manager
        # For now, return movies from the same genre
        movies = movie_manager.advanced_filter(limit=limit)
        
        # Find the target movie to get its genre
        target_movie = None
        for movie in movies:
            if movie.id == movie_id:
                target_movie = movie
                break
        
        if not target_movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Get movies with similar genres
        if target_movie.genres:
            similar_movies = movie_manager.advanced_filter(
                genres=[target_movie.genres.split(',')[0].strip()],
                limit=limit
            )
            return [MovieResponse.from_orm(movie) for movie in similar_movies]
        else:
            return []
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching similar movies: {str(e)}")


@router.get("/{user_id}/preferences")
async def get_user_preferences(user_id: int):
    """Get user preferences based on watch history."""
    try:
        # TODO: Implement user preferences in movie_manager
        # For now, return basic stats
        history = movie_manager.get_watch_history(user_id=user_id, limit=1000)
        
        if not history:
            return {
                "message": "No watch history available",
                "preferences": {}
            }
        
        # Calculate genre preferences
        genre_counts = {}
        for entry in history:
            genres = entry['movie']['genres']
            if genres:
                for genre in genres.split(','):
                    genre = genre.strip()
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Get top genres
        top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate average rating
        rated_movies = [entry for entry in history if entry['rating'] is not None]
        avg_rating = sum(entry['rating'] for entry in rated_movies) / len(rated_movies) if rated_movies else 0
        
        return {
            "user_id": user_id,
            "preferences": {
                "favorite_genres": [genre for genre, count in top_genres],
                "average_rating": round(avg_rating, 1),
                "total_watched": len(history),
                "total_rated": len(rated_movies)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user preferences: {str(e)}") 