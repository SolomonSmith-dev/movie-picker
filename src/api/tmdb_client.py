"""TMDb API client for MoviePicker application."""

import time
from typing import Dict, List, Optional
import requests

from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TMDbClient:
    """Client for interacting with The Movie Database (TMDb) API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.tmdb_api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        self.session.params.update({"api_key": self.api_key})

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict]:
        """Search for a movie by title and optional year."""
        try:
            params = {"query": title, "include_adult": False}

            if year:
                params["year"] = year

            response = self.session.get(f"{self.base_url}/search/movie", params=params)
            response.raise_for_status()

            data = response.json()
            if data.get("results"):
                return data["results"][0]  # Return first match

            logger.warning(f"No TMDb results found for: {title} ({year})")
            return None

        except requests.RequestException as e:
            logger.error(f"TMDb search failed for {title}: {e}")
            return None

    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a movie."""
        try:
            response = self.session.get(f"{self.base_url}/movie/{movie_id}")
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to get movie details for ID {movie_id}: {e}")
            return None

    def get_movie_credits(self, movie_id: int) -> Optional[Dict]:
        """Get cast and crew information for a movie."""
        try:
            response = self.session.get(f"{self.base_url}/movie/{movie_id}/credits")
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to get credits for movie ID {movie_id}: {e}")
            return None

    def get_movie_images(self, movie_id: int) -> Optional[Dict]:
        """Get images (posters, backdrops) for a movie."""
        try:
            response = self.session.get(f"{self.base_url}/movie/{movie_id}/images")
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to get images for movie ID {movie_id}: {e}")
            return None

    def enrich_movie_data(self, movie_data: Dict) -> Dict:
        """Enrich movie data with TMDb information."""
        title = movie_data.get("title")
        year = movie_data.get("year")

        if not title:
            return movie_data

        # Search for the movie
        search_result = self.search_movie(title, year)
        if not search_result:
            return movie_data

        movie_id = search_result["id"]

        # Get detailed information
        details = self.get_movie_details(movie_id)
        credits = self.get_movie_credits(movie_id)
        images = self.get_movie_images(movie_id)

        if not details:
            return movie_data

        # Update movie data with TMDb information
        enriched_data = movie_data.copy()

        # Basic details
        if not enriched_data.get("tmdb_id"):
            enriched_data["tmdb_id"] = movie_id

        if not enriched_data.get("overview") and details.get("overview"):
            enriched_data["overview"] = details["overview"]

        if not enriched_data.get("runtime") and details.get("runtime"):
            enriched_data["runtime"] = details["runtime"]

        if not enriched_data.get("language") and details.get("original_language"):
            enriched_data["language"] = details["original_language"]

        if not enriched_data.get("country") and details.get("production_countries"):
            countries = [c["name"] for c in details["production_countries"]]
            enriched_data["country"] = ", ".join(countries)

        # Genres
        if not enriched_data.get("genres") or enriched_data["genres"].lower() in [
            "",
            "unknown genres",
        ]:
            if details.get("genres"):
                genres = [g["name"] for g in details["genres"]]
                enriched_data["genres"] = ", ".join(genres)

        # Director
        if not enriched_data.get("director") or enriched_data["director"].lower() in [
            "",
            "unknown director",
        ]:
            if credits and credits.get("crew"):
                directors = [
                    person["name"]
                    for person in credits["crew"]
                    if person.get("job") == "Director"
                ]
                if directors:
                    enriched_data["director"] = ", ".join(directors)

        # Cast
        if not enriched_data.get("cast"):
            if credits and credits.get("cast"):
                top_cast = [person["name"] for person in credits["cast"][:5]]
                enriched_data["cast"] = ", ".join(top_cast)

        # Poster URL
        if not enriched_data.get("poster_url"):
            if images and images.get("posters"):
                # Get the first poster (usually the main one)
                poster = images["posters"][0]
                poster_path = poster.get("file_path")
                if poster_path:
                    enriched_data["poster_url"] = (
                        f"https://image.tmdb.org/t/p/w500{poster_path}"
                    )

        # Rating
        if not enriched_data.get("rating") and details.get("vote_average"):
            enriched_data["rating"] = details["vote_average"]

        # Year (if missing)
        if not enriched_data.get("year") and details.get("release_date"):
            enriched_data["year"] = details["release_date"].split("-")[0]

        logger.info(f"Enriched movie: {title}")
        return enriched_data

    def batch_enrich_movies(
        self, movies: List[Dict], delay: float = 0.25
    ) -> List[Dict]:
        """Enrich a batch of movies with rate limiting."""
        enriched_movies = []

        for i, movie in enumerate(movies):
            try:
                enriched_movie = self.enrich_movie_data(movie)
                enriched_movies.append(enriched_movie)

                # Rate limiting
                if i < len(movies) - 1:  # Don't delay after the last movie
                    time.sleep(delay)

            except Exception as e:
                logger.error(f"Failed to enrich movie {movie.get('title')}: {e}")
                enriched_movies.append(movie)  # Keep original data

        logger.info(f"Enriched {len(enriched_movies)} movies")
        return enriched_movies

    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """Get popular movies from TMDb."""
        try:
            response = self.session.get(
                f"{self.base_url}/movie/popular", params={"page": page}
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to get popular movies: {e}")
            return None

    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict]:
        """Get top rated movies from TMDb."""
        try:
            response = self.session.get(
                f"{self.base_url}/movie/top_rated", params={"page": page}
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to get top rated movies: {e}")
            return None


# Global TMDb client instance
tmdb_client = TMDbClient()
