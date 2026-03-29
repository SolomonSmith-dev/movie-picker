#!/usr/bin/env python3
"""Initialize MoviePicker 2.0 project structure and database."""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config import ensure_directories, settings
from src.utils.logger import setup_logger
from src.core.migrations import run_migrations


def main():
    """Initialize the MoviePicker 2.0 project."""
    print("🎬 Initializing MoviePicker 2.0...")

    # Set up logging
    logger = setup_logger("moviepicker", log_file="init.log")

    try:
        # Ensure directories exist
        print("📁 Creating directories...")
        ensure_directories()

        # Check for TMDb API key
        if (
            not settings.tmdb_api_key
            or settings.tmdb_api_key == "your_tmdb_api_key_here"
        ):
            print("⚠️  Warning: TMDb API key not configured.")
            print("   Please set TMDB_API_KEY in your .env file")
            print("   Get a free API key at: https://www.themoviedb.org/settings/api")

        # Initialize database
        print("🗄️  Initializing database...")
        run_migrations()

        print("✅ MoviePicker 2.0 initialization completed successfully!")
        print("\n🎯 Next steps:")
        print("   1. Set up your TMDb API key in .env file")
        print("   2. Run: python src/ui/cli_interface.py")
        print("   3. For development: pip install -r requirements-dev.txt")

    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        print(f"❌ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
