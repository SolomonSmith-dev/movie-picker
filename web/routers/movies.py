"""Movies API router for MoviePicker."""

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

# Add src to path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.movie_manager import movie_manager

router = APIRouter(prefix="/movies", tags=["movies"])


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


class MovieListResponse(BaseModel):
    """Movie list response model."""

    movies: List[MovieResponse]
    total: int
    page: int
    per_page: int


@router.get("/", response_model=MovieListResponse)
async def list_movies(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Movies per page"),
    search: Optional[str] = Query(None, description="Search term"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    year_min: Optional[int] = Query(None, description="Minimum year"),
    year_max: Optional[int] = Query(None, description="Maximum year"),
    rating_min: Optional[float] = Query(
        None, ge=0, le=10, description="Minimum rating"
    ),
    rating_max: Optional[float] = Query(
        None, ge=0, le=10, description="Maximum rating"
    ),
    order_by: str = Query(
        "rating", description="Order by field (rating, year, title, runtime)"
    ),
    order_direction: str = Query("desc", description="Order direction (asc, desc)"),
):
    """List movies with optional filtering and search."""

    try:
        if search:
            # Use fuzzy search
            movies = movie_manager.search_movies(search, limit=per_page)
        else:
            # Use advanced filtering
            movies = movie_manager.advanced_filter(
                year_min=year_min,
                year_max=year_max,
                rating_min=rating_min,
                rating_max=rating_max,
                genres=[genre] if genre else None,
                order_by=order_by,
                order_direction=order_direction,
                limit=per_page,
            )

        # Convert to response models
        movie_responses = [MovieResponse.from_orm(movie) for movie in movies]

        return MovieListResponse(
            movies=movie_responses,
            total=len(movie_responses),  # TODO: Get actual total count
            page=page,
            per_page=per_page,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movies: {str(e)}")


@router.get("/movie-of-the-day", response_model=MovieResponse)
async def get_movie_of_the_day():
    """Get the movie of the day."""
    try:
        movie = movie_manager.get_movie_of_the_day()

        if not movie:
            raise HTTPException(status_code=404, detail="No movie available for today")

        return MovieResponse.from_orm(movie)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting movie of the day: {str(e)}"
        )


@router.get("/random/pick", response_model=MovieResponse)
async def pick_random_movie(
    exclude_watched: bool = Query(True, description="Exclude watched movies"),
):
    """Pick a random movie."""
    try:
        movies = movie_manager.advanced_filter(exclude_watched=exclude_watched, limit=1)

        if not movies:
            raise HTTPException(status_code=404, detail="No movies available")

        return MovieResponse.from_orm(movies[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error picking random movie: {str(e)}"
        )


@router.get("/top-rated", response_model=List[MovieResponse])
async def get_top_rated_movies(
    limit: int = Query(10, ge=1, le=50, description="Number of movies to return"),
):
    """Get top rated movies."""
    try:
        movies = movie_manager.get_top_rated_movies(limit=limit)
        return [MovieResponse.from_orm(movie) for movie in movies]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top rated movies: {str(e)}"
        )


@router.get("/recent", response_model=List[MovieResponse])
async def get_recent_movies(
    limit: int = Query(10, ge=1, le=50, description="Number of movies to return"),
):
    """Get recent movies."""
    try:
        movies = movie_manager.get_recent_movies(limit=limit)
        # Filter out movies with invalid years
        valid_movies = [
            movie for movie in movies if movie.year and isinstance(movie.year, int)
        ]
        return [MovieResponse.from_orm(movie) for movie in valid_movies[:limit]]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching recent movies: {str(e)}"
        )


@router.get("/stats")
async def get_movie_stats():
    """Get movie statistics."""
    try:
        stats = movie_manager.get_filter_stats()
        return stats

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching movie stats: {str(e)}"
        )


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int):
    """Get a specific movie by ID."""
    try:
        # For now, we'll search through all movies
        # TODO: Add a direct get_by_id method to movie_manager
        movies = movie_manager.advanced_filter(limit=1000)  # Get all movies
        movie = next((m for m in movies if m.id == movie_id), None)

        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        return MovieResponse.from_orm(movie)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching movie: {str(e)}")
