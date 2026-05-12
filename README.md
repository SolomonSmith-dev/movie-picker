# movie-picker

A movie recommendation and management system built with Python, FastAPI, and SQLAlchemy. Integrates with the TMDb API for metadata enrichment.

## Features

- Smart recommendations based on watch history and preferences
- Filter by genre, year, director, actor, and rating
- Fuzzy search across titles, directors, and cast
- Watch history tracking with favorites and ratings
- TMDb integration for posters, cast, ratings, and metadata

## Stack

Python, FastAPI, SQLAlchemy, SQLite, TMDb API.

## Setup

```bash
git clone https://github.com/SolomonSmith-dev/movie-picker
cd movie-picker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# Add your TMDb API key to .env
python -m src.core.migrations
python src/ui/cli_interface.py
```

Get a TMDb API key at [themoviedb.org](https://www.themoviedb.org/settings/api).

## Project layout

```
src/      # core, ui, recommendation logic
tests/    # pytest suite
lists/    # curated movie lists
data/     # SQLite DB + TMDb cache (gitignored when large)
web/      # FastAPI web layer
```

## License

MIT.
