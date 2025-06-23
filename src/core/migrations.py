"""Database migration utilities for MoviePicker application."""

import json
from pathlib import Path
from typing import List, Dict
from sqlalchemy import and_

from .database import db_manager
from .models import Movie, User, WatchHistory, UserRating
from .movie_manager import movie_manager
from ..utils.config import get_movie_data_path
from ..utils.logger import get_logger

logger = get_logger(__name__)


def create_initial_schema():
    """Create the initial database schema."""
    try:
        db_manager.create_tables()
        logger.info("Initial database schema created successfully")
    except Exception as e:
        logger.error(f"Failed to create database schema: {e}")
        raise


def import_initial_data():
    """Import initial movie data from JSON files."""
    try:
        # Import standardized movies
        standardized_movies = movie_manager.load_movies_from_json("standardized_movies_enriched.json")
        if standardized_movies:
            count = movie_manager.import_movies_to_database(standardized_movies)
            logger.info(f"Imported {count} standardized movies")
        
        # Import Plex movies
        plex_movies = movie_manager.load_movies_from_json("plex_movies_enriched.json")
        if plex_movies:
            count = movie_manager.import_movies_to_database(plex_movies)
            logger.info(f"Imported {count} Plex movies")
        
        # Create default user
        create_default_user()
        
        logger.info("Initial data import completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to import initial data: {e}")
        raise


def create_default_user():
    """Create a default user for the application."""
    try:
        with db_manager.get_session() as session:
            # Check if default user already exists
            existing_user = session.query(User).filter(User.username == "default").first()
            if existing_user:
                logger.info("Default user already exists")
                return
            
            # Create default user
            default_user = User(
                username="default",
                email="default@moviepicker.local",
                preferences=json.dumps({
                    "favorite_genres": [],
                    "excluded_genres": [],
                    "min_rating": 0,
                    "max_year": None,
                    "min_year": None
                })
            )
            
            session.add(default_user)
            session.commit()
            logger.info("Default user created successfully")
            
    except Exception as e:
        logger.error(f"Failed to create default user: {e}")
        raise


def migrate_from_old_format():
    """Migrate data from the old JSON-based format to the new database format."""
    try:
        # Check if database is empty
        with db_manager.get_session() as session:
            movie_count = session.query(Movie).count()
            if movie_count > 0:
                logger.info("Database already contains movies, skipping migration")
                return
        
        # Import movies from old format
        import_initial_data()
        
        # Migrate watch history from old history.txt file
        migrate_watch_history()
        
        logger.info("Migration from old format completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to migrate from old format: {e}")
        raise


def migrate_watch_history():
    """Migrate watch history from the old history.txt file."""
    try:
        history_file = Path("history.txt")
        if not history_file.exists():
            logger.info("No history.txt file found, skipping history migration")
            return
        
        with db_manager.get_session() as session:
            # Get default user
            default_user = session.query(User).filter(User.username == "default").first()
            if not default_user:
                logger.warning("No default user found, cannot migrate history")
                return
            
            migrated_count = 0
            
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # Parse the old format: "2024-01-01 | Movie Title (2020) | Director | Genres ❤️"
                        parts = line.split(" | ")
                        if len(parts) >= 3:
                            date_str = parts[0]
                            title_year = parts[1]
                            director = parts[2]
                            
                            # Extract title and year
                            if " (" in title_year and title_year.endswith(")"):
                                title = title_year.rsplit(" (", 1)[0]
                                year_str = title_year.rsplit(" (", 1)[1].rstrip(")")
                                year = int(year_str) if year_str.isdigit() else None
                            else:
                                title = title_year
                                year = None
                            
                            # Check if movie exists
                            movie = session.query(Movie).filter(
                                Movie.title == title,
                                Movie.year == year
                            ).first()
                            
                            if movie:
                                # Check if already watched
                                existing = session.query(WatchHistory).filter(
                                    and_(
                                        WatchHistory.user_id == default_user.id,
                                        WatchHistory.movie_id == movie.id
                                    )
                                ).first()
                                
                                if not existing:
                                    # Create watch history entry
                                    is_favorite = "❤️" in line
                                    watch_history = WatchHistory(
                                        user_id=default_user.id,
                                        movie_id=movie.id,
                                        is_favorite=is_favorite
                                    )
                                    session.add(watch_history)
                                    migrated_count += 1
                    
                    except Exception as e:
                        logger.warning(f"Failed to parse history line: {line} - {e}")
                        continue
            
            session.commit()
            logger.info(f"Migrated {migrated_count} watch history entries")
        
    except Exception as e:
        logger.error(f"Failed to migrate watch history: {e}")
        raise


def run_migrations():
    """Run all necessary migrations."""
    try:
        logger.info("Starting database migrations...")
        
        # Create schema
        create_initial_schema()
        
        # Migrate data
        migrate_from_old_format()
        
        logger.info("Database migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Database migrations failed: {e}")
        raise


if __name__ == "__main__":
    run_migrations() 