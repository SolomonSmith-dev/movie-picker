#!/usr/bin/env python3
"""Test script for MoviePicker API endpoints."""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test an API endpoint and print results."""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Status: {response.status_code}")
            if isinstance(result, dict) and 'movies' in result:
                print(f"   📊 Found {len(result['movies'])} movies")
            elif isinstance(result, list):
                print(f"   📊 Found {len(result)} items")
            elif isinstance(result, dict) and 'recommendations' in result:
                print(f"   📊 Found {result['total_recommendations']} recommendations")
            return True
        else:
            print(f"   ❌ Failed! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Test all API endpoints."""
    print("🎬 MoviePicker API Endpoint Tests")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/", description="Root endpoint")
    test_endpoint("/docs", description="API documentation")
    
    # Test movies endpoints
    test_endpoint("/movies/", description="List movies")
    test_endpoint("/movies/?per_page=3", description="List movies with pagination")
    test_endpoint("/movies/?search=batman", description="Search movies")
    test_endpoint("/movies/?genre=Action", description="Filter by genre")
    test_endpoint("/movies/movie-of-the-day", description="Movie of the day")
    test_endpoint("/movies/random/pick", description="Random movie picker")
    test_endpoint("/movies/top-rated", description="Top rated movies")
    test_endpoint("/movies/recent", description="Recent movies")
    test_endpoint("/movies/stats", description="Movie statistics")
    test_endpoint("/movies/1", description="Get specific movie")
    
    # Test users endpoints
    test_endpoint("/users/", description="List users")
    test_endpoint("/users/1", description="Get specific user")
    test_endpoint("/users/1/watch-history", description="User watch history")
    test_endpoint("/users/1/stats", description="User statistics")
    
    # Test recommendations endpoints
    test_endpoint("/recommendations/1", description="User recommendations")
    test_endpoint("/recommendations/1/personalized", description="Personalized recommendations")
    test_endpoint("/recommendations/1/surprise", description="Surprise recommendation")
    test_endpoint("/recommendations/1/preferences", description="User preferences")
    test_endpoint("/recommendations/1/similar/1", description="Similar movies")
    
    # Test POST endpoints
    test_endpoint(
        "/users/1/watch-history", 
        method="POST", 
        data={"movie_id": 2, "rating": 8.5},
        description="Mark movie as watched with rating"
    )
    
    print("\n🎉 API Testing Complete!")
    print(f"📖 View interactive docs at: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 