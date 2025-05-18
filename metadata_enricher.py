# This script enriches a list of movies with additional metadata from TMDb.
# It searches for each movie by title and year, retrieves details and credits,
# and updates the movie's genres, director, year, and cast fields if they are missing
# or marked as unknown. The enriched list is saved to a new JSON file.

import json
import requests
import time
import argparse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# Ensure you have a .env file with your TMDB_API_KEY
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Check if the API key is set
def search_tmdb(title, year=None):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "year": year,
        "include_adult": False
    }
    response = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params)
    if response.status_code == 200 and response.json()["results"]:
        return response.json()["results"][0]
    print(f"[!] Search failed for: {title} ({year})")
    return None

# Function to get movie details and credits
# from TMDb using the movie ID
def get_movie_details(movie_id):
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Function to get movie credits from TMDb using the movie ID
def get_movie_credits(movie_id):
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}/credits", params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Function to enrich a movie with TMDb data
def enrich_movie(movie):
    title = movie.get("title")
    year = movie.get("year")
    if not title:
        return movie

    search_result = search_tmdb(title, year)
    if not search_result:
        return movie  # No match found

    movie_id = search_result["id"]
    details = get_movie_details(movie_id)
    credits = get_movie_credits(movie_id)
    if not details or not credits:
        print(f"[!] Failed to retrieve full data for: {title}")
        return movie

    # Update fields only if missing or marked unknown
    if movie.get("genres", "").lower() in ["", "unknown genres"]:
        movie["genres"] = ", ".join([g["name"] for g in details.get("genres", [])])

    # Check if the director is missing or marked as unknown
    if movie.get("director", "").lower() in ["", "unknown director"]:
        crew = credits.get("crew", [])
        directors = [person["name"] for person in crew if person.get("job") == "Director"]
        if directors:
            movie["director"] = ", ".join(directors)
        else:
            print(f"[!] No director found for {title}")
    # Check if the year is missing or marked as unknown
    if movie.get("year", "").lower() in ["", "unknown year"]:
        date = details.get("release_date", "")
        if date:
            movie["year"] = date.split("-")[0]
    # Check if the cast is missing or marked as unknown
    if "cast" not in movie or not movie["cast"]:
        cast = credits.get("cast", [])
        top_cast = [person["name"] for person in cast[:5]]
        movie["cast"] = ", ".join(top_cast)

    return movie
# Main function to handle command line arguments and process the input JSON
def main():
    parser = argparse.ArgumentParser(description="Enrich movie JSON with TMDb data.")
    parser.add_argument("--input", required=True, help="Path to the input JSON file")
    parser.add_argument("--output", required=True, help="Path to write the enriched JSON output")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        movies = json.load(f)

    enriched = []
    for movie in movies:
        enriched_movie = enrich_movie(movie)
        enriched.append(enriched_movie)
        print(f"✅ Processed: {enriched_movie['title']}")
        time.sleep(0.25)  # TMDb rate limit protection

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=4)

    print(f"\n✅ Enrichment complete. Output written to {args.output}")

if __name__ == "__main__":
    main()
