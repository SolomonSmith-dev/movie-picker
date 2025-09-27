# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development

# Set up environment variables
cp env.example .env
# Edit .env and add your TMDb API key
```

### Database Operations
```bash
# Initialize/migrate database
python -m src.core.migrations

# Reset database (if needed)
rm -f data/moviepicker.db
python -m src.core.migrations
```

### Running the Application
```bash
# CLI interface (main entry point)
python src/ui/cli_interface.py

# Web API server
uvicorn src.ui.web_interface:app --reload

# Frontend development server (React/Vite)
cd web/frontend
npm install
npm run dev
```

### Testing
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest test_advanced_filtering.py
pytest test_api_endpoints.py

# Run tests with specific markers
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

### Code Quality
```bash
# Format code
black src/
isort src/

# Type checking
mypy src/

# Linting
flake8 src/

# Run all quality checks
black src/ && isort src/ && mypy src/ && flake8 src/

# Frontend linting
cd web/frontend && npm run lint
```

## Architecture Overview

MoviePicker is a hybrid Python application with both CLI and web interfaces, using a SQLAlchemy-based database backend with FastAPI web services.

### Core Architecture Layers

**Data Layer (`src/core/`)**:
- `models.py` - SQLAlchemy models (Movie, User, WatchHistory, UserRating, MovieNight)
- `database.py` - Database connection and session management
- `migrations.py` - Database schema initialization and migrations

**Business Logic (`src/core/`)**:
- `movie_manager.py` - Central movie operations manager (recommendations, filtering, watch history)
- `recommendation.py` - AI-powered recommendation engine
- `filters.py` - Advanced movie filtering and search functionality

**API Layer (`src/api/`)**:
- `tmdb_client.py` - TMDb API integration for movie metadata
- `enricher.py` - Data enrichment pipeline

**Interface Layer (`src/ui/`)**:
- `cli_interface.py` - Command-line interface (primary interface)
- `web_interface.py` - FastAPI web server

**Web Frontend (`web/frontend/`)**:
- React/TypeScript SPA with Vite build system
- Tailwind CSS for styling, React Query for API state management
- Component-based architecture with modern React patterns

### Key Design Patterns

**Dual Interface Design**: The application maintains both CLI and web interfaces sharing the same business logic through `movie_manager.py`. The CLI is the primary interface, while the web interface is under development.

**Database Abstraction**: Uses SQLAlchemy ORM with a centralized `db_manager` for session handling. All database operations go through the business logic layer, not directly from interfaces.

**External API Integration**: TMDb integration is abstracted through dedicated client classes, with data enrichment handled separately from core movie operations.

**Recommendation System**: AI-powered recommendations use user watch history and ratings to provide personalized suggestions through the `RecommendationEngine`.

### Data Flow

1. **Movie Data**: Loaded from JSON files in `lists/` directory, enriched via TMDb API, stored in SQLAlchemy database
2. **User Interactions**: CLI commands → `movie_manager` → database operations → response formatting
3. **Web API**: FastAPI endpoints → `movie_manager` → database operations → JSON response
4. **Frontend**: React components → API calls → state management → UI updates

### Configuration

- Environment variables managed through `.env` file (use `env.example` as template)
- Main config in `pyproject.toml` with tool configurations for Black, isort, mypy, pytest
- Database connection strings and API keys configured via environment variables

## Project Structure Context

**Legacy Files**: `moviepicker.py` is the original implementation - use `src/ui/cli_interface.py` for current CLI interface.

**Data Directory**: `data/` contains movie JSON files, configuration, and logs. The `lists/` directory contains enriched movie data files.

**Testing Strategy**: Both unit tests (in `tests/`) and standalone test files (`test_*.py` in root) for integration testing. Uses pytest with coverage reporting.

**Web Development**: The web interface is built with modern React practices - use `web/frontend/` for frontend development, backend API routes in `web/routers/`.

## TMDb Integration

The application heavily relies on TMDb API for movie metadata enrichment. Ensure `TMDB_API_KEY` is set in `.env` file. The enrichment process updates movie records with:
- Poster URLs and images
- Cast and crew information  
- Updated ratings and metadata
- Movie overviews and descriptions

Run `python metadata_enricher.py` to manually trigger data enrichment for existing movie records.