#!/usr/bin/env python3
"""Test script for advanced filtering functionality."""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.movie_manager import movie_manager


def test_filtering():
    """Test the advanced filtering system."""
    print("🧪 Testing Advanced Filtering System")
    print("=" * 50)

    # Test 1: Get filter statistics
    print("\n1. Testing Filter Statistics...")
    try:
        stats = movie_manager.get_filter_stats()
        print(f"✅ Total movies: {stats['total_movies']}")
        print(
            f"✅ Year range: {stats['year_range']['min']} - {stats['year_range']['max']}"
        )
        print(
            f"✅ Rating range: {stats['rating_range']['min']:.1f} - {stats['rating_range']['max']:.1f}"
        )
        print(f"✅ Available genres: {len(stats['available_genres'])}")
        print(f"✅ Available languages: {len(stats['available_languages'])}")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

    # Test 2: Filter by year range
    print("\n2. Testing Year Range Filter...")
    try:
        movies = movie_manager.advanced_filter(year_min=2020, year_max=2023, limit=5)
        print(f"✅ Found {len(movies)} movies from 2020-2023")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie.title} ({movie.year})")
    except Exception as e:
        print(f"❌ Error filtering by year: {e}")

    # Test 3: Filter by rating
    print("\n3. Testing Rating Filter...")
    try:
        movies = movie_manager.advanced_filter(rating_min=8.0, limit=5)
        print(f"✅ Found {len(movies)} movies with rating >= 8.0")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie.title} ({movie.rating}/10)")
    except Exception as e:
        print(f"❌ Error filtering by rating: {e}")

    # Test 4: Filter by genre
    print("\n4. Testing Genre Filter...")
    try:
        movies = movie_manager.advanced_filter(genres=["Action"], limit=5)
        print(f"✅ Found {len(movies)} Action movies")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie.title} ({movie.genres})")
    except Exception as e:
        print(f"❌ Error filtering by genre: {e}")

    # Test 5: Fuzzy search
    print("\n5. Testing Fuzzy Search...")
    try:
        movies = movie_manager.search_movies("batman", limit=5)
        print(f"✅ Found {len(movies)} movies matching 'batman'")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie.title} ({movie.year})")
    except Exception as e:
        print(f"❌ Error in fuzzy search: {e}")

    # Test 6: Multi-criteria filter
    print("\n6. Testing Multi-Criteria Filter...")
    try:
        movies = movie_manager.advanced_filter(
            year_min=2010, rating_min=7.0, genres=["Drama"], limit=5
        )
        print(f"✅ Found {len(movies)} Drama movies from 2010+ with rating >= 7.0")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie.title} ({movie.year}) - {movie.rating}/10")
    except Exception as e:
        print(f"❌ Error in multi-criteria filter: {e}")

    print("\n🎉 Advanced Filtering Test Complete!")


if __name__ == "__main__":
    test_filtering()
