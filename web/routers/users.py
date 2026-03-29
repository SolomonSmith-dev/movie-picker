"""Users API router for MoviePicker."""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Add src to path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.movie_manager import movie_manager

router = APIRouter(prefix="/users", tags=["users"])


class UserResponse(BaseModel):
    """User response model."""

    id: int
    username: str
    email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation model."""

    username: str
    email: Optional[str] = None


class WatchHistoryResponse(BaseModel):
    """Watch history response model."""

    movie_id: int
    movie_title: str
    movie_year: Optional[int] = None
    movie_director: Optional[str] = None
    movie_genres: Optional[str] = None
    movie_rating: Optional[float] = None
    watched_at: datetime
    user_rating: Optional[float] = None

    class Config:
        from_attributes = True


class MarkWatchedRequest(BaseModel):
    """Mark movie as watched request model."""

    movie_id: int
    rating: Optional[float] = None


@router.get("/", response_model=List[UserResponse])
async def list_users():
    """List all users."""
    try:
        # TODO: Implement user listing in movie_manager
        # For now, return a default user
        return [
            UserResponse(
                id=1, username="default_user", email=None, created_at=datetime.now()
            )
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user."""
    try:
        # TODO: Implement user creation in movie_manager
        # For now, return a mock user
        return UserResponse(
            id=1, username=user.username, email=user.email, created_at=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a specific user by ID."""
    try:
        # TODO: Implement user retrieval in movie_manager
        # For now, return a mock user
        return UserResponse(
            id=user_id, username="default_user", email=None, created_at=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


@router.get("/{user_id}/watch-history", response_model=List[WatchHistoryResponse])
async def get_watch_history(
    user_id: int,
    limit: int = Query(20, ge=1, le=100, description="Number of entries to return"),
):
    """Get user's watch history."""
    try:
        history = movie_manager.get_watch_history(user_id=user_id, limit=limit)

        # Convert to response format
        history_responses = []
        for entry in history:
            movie = entry["movie"]
            history_responses.append(
                WatchHistoryResponse(
                    movie_id=movie["id"],
                    movie_title=movie["title"],
                    movie_year=movie["year"],
                    movie_director=movie["director"],
                    movie_genres=movie["genres"],
                    movie_rating=movie["rating"],
                    watched_at=entry["watched_at"],
                    user_rating=entry["rating"],
                )
            )

        return history_responses

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching watch history: {str(e)}"
        )


@router.post("/{user_id}/watch-history")
async def mark_as_watched(user_id: int, request: MarkWatchedRequest):
    """Mark a movie as watched for a user."""
    try:
        success = movie_manager.mark_as_watched(
            movie_id=request.movie_id, user_id=user_id, rating=request.rating
        )

        if success:
            return {"message": "Movie marked as watched successfully"}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to mark movie as watched"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error marking movie as watched: {str(e)}"
        )


@router.get("/{user_id}/stats")
async def get_user_stats(user_id: int):
    """Get user statistics."""
    try:
        history = movie_manager.get_watch_history(user_id=user_id, limit=1000)

        if not history:
            return {
                "total_watched": 0,
                "average_rating": 0.0,
                "favorite_genres": [],
                "total_movies_rated": 0,
            }

        total_watched = len(history)
        rated_movies = [entry for entry in history if entry["rating"] is not None]
        total_rated = len(rated_movies)

        if rated_movies:
            avg_rating = sum(entry["rating"] for entry in rated_movies) / total_rated
        else:
            avg_rating = 0.0

        # Calculate favorite genres
        genre_counts = {}
        for entry in history:
            genres = entry["movie"]["genres"]
            if genres:
                for genre in genres.split(","):
                    genre = genre.strip()
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1

        favorite_genres = sorted(
            genre_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
        favorite_genres = [genre for genre, count in favorite_genres]

        return {
            "total_watched": total_watched,
            "average_rating": round(avg_rating, 1),
            "favorite_genres": favorite_genres,
            "total_movies_rated": total_rated,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching user stats: {str(e)}"
        )
