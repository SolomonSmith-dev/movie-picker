# MoviePicker

A movie recommendation and management system built with Python, FastAPI, and SQLAlchemy. Integrates with the TMDb API for metadata enrichment.

## Features

- Smart recommendations based on watch history and preferences
- Filter by genre, year, director, actor, and rating
- Fuzzy search across titles, directors, and cast
- Watch history tracking with favorites and ratings
- TMDb integration for posters, cast, ratings, and metadata

## Stack

Python, FastAPI, SQLAlchemy, SQLite, TMDb API

## Environment Setup

> **Required:** Copy `env.example` to `.env` and fill in your API keys before running the app.
>
> ```bash
> cp env.example .env
> # Open .env and set TMDB_API_KEY (and any other keys you need)
> ```
>
> Get a free TMDb API key at [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api).

## Setup

```bash
git clone https://github.com/SolomonSmith-dev/MoviePicker
cd MoviePicker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env          # then add your TMDB_API_KEY
python -m src.core.migrations
python src/ui/cli_interface.py
```

## License

MIT
