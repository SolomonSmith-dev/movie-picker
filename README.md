# 🎬 MoviePicker 2.0

Welcome to **MoviePicker 2.0** — a modern, feature-rich movie recommendation and management system built with Python, FastAPI, and SQLAlchemy.

## 🚀 Features

### Core Features
- 🎥 **Smart Movie Recommendations** - AI-powered suggestions based on your preferences
- 🎭 **Advanced Filtering** - Filter by genre, year, director, actor, rating, and more
- 🔍 **Powerful Search** - Fuzzy search across titles, directors, and cast
- 📊 **Watch History & Analytics** - Track your viewing habits and get insights
- ❤️ **Favorites & Ratings** - Rate movies and mark favorites for rewatch
- 👥 **User Profiles** - Personalized recommendations and preferences
- 🌐 **Web Interface** - Modern web UI built with FastAPI and React

### Advanced Features
- 🎬 **Movie Nights** - Plan group watching sessions with voting
- 📱 **Streaming Integration** - See where movies are available to stream
- 🔄 **Data Enrichment** - Automatic metadata fetching from TMDb
- 📈 **Analytics Dashboard** - View watching patterns and statistics
- 🔔 **Notifications** - Get daily movie recommendations
- 🗄️ **Database Backend** - Robust SQLAlchemy-based data storage

## 🏗️ Architecture

```
MoviePicker/
├── src/                          # Source code
│   ├── core/                     # Core business logic
│   │   ├── models.py             # Database models
│   │   ├── database.py           # Database management
│   │   ├── movie_manager.py      # Movie operations
│   │   └── migrations.py         # Database migrations
│   ├── api/                      # API clients
│   │   ├── tmdb_client.py        # TMDb API integration
│   │   └── enricher.py           # Data enrichment
│   ├── ui/                       # User interfaces
│   │   ├── cli_interface.py      # Command-line interface
│   │   └── web_interface.py      # Web interface (coming soon)
│   └── utils/                    # Utilities
│       ├── config.py             # Configuration management
│       └── logger.py             # Logging utilities
├── tests/                        # Test suite
├── data/                         # Data files
│   ├── movies/                   # Movie JSON files
│   ├── config/                   # Configuration files
│   └── logs/                     # Application logs
├── web/                          # Web interface assets
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml               # Modern Python packaging
└── setup.py                     # Package setup
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- TMDb API key (get one at [themoviedb.org](https://www.themoviedb.org/settings/api))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MoviePicker.git
   cd MoviePicker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your TMDb API key
   ```

5. **Initialize the database**
   ```bash
   python -m src.core.migrations
   ```

6. **Run the application**
   ```bash
   # CLI version
   python src/ui/cli_interface.py
   
   # Web version (coming soon)
   uvicorn src.ui.web_interface:app --reload
   ```

## 🎯 Usage

### Command Line Interface

```bash
# Start the CLI
python src/ui/cli_interface.py

# Available options:
# 1. Pick from Greatest Movies
# 2. Pick from My Plex Movies  
# 3. Pick by Genre
# 4. View Watch History
# 5. Reset Watch History
# 6. Rewatch a Favorite
# 7. Search by Director
# 8. Search by Actor
```

### Web Interface (Coming Soon)

The web interface will provide:
- Modern, responsive design
- Advanced filtering and search
- Movie recommendations
- Watch history and analytics
- User profiles and preferences
- Movie night planning

## 🔧 Development

### Setting up Development Environment

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Code formatting**
   ```bash
   black src/
   isort src/
   ```

5. **Type checking**
   ```bash
   mypy src/
   ```

### Project Structure

- **`src/core/`** - Core business logic and database models
- **`src/api/`** - External API integrations (TMDb, JustWatch)
- **`src/ui/`** - User interfaces (CLI, web)
- **`src/utils/`** - Shared utilities (config, logging)
- **`tests/`** - Test suite with unit and integration tests
- **`data/`** - Application data and configuration

## 📊 Database Schema

The application uses SQLAlchemy with the following main models:

- **`Movie`** - Movie information and metadata
- **`User`** - User profiles and preferences
- **`WatchHistory`** - Track watched movies and favorites
- **`UserRating`** - User ratings and reviews
- **`MovieNight`** - Group watching sessions
- **`MovieNightVote`** - Votes for movie nights

## 🔌 API Integration

### TMDb Integration
- Automatic metadata enrichment
- Poster images and backdrops
- Cast and crew information
- Ratings and reviews
- Popular and top-rated movies

### JustWatch Integration (Coming Soon)
- Streaming availability
- Platform-specific information
- Regional availability

## 🚀 Deployment

### Docker Deployment

```bash
# Build the image
docker build -t moviepicker .

# Run the container
docker run -p 8000:8000 moviepicker
```

### Production Deployment

1. **Set up a production database** (PostgreSQL recommended)
2. **Configure environment variables**
3. **Set up reverse proxy** (nginx)
4. **Configure SSL certificates**
5. **Set up monitoring and logging**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TMDb](https://www.themoviedb.org/) for movie data and API
- [JustWatch](https://www.justwatch.com/) for streaming availability
- The open-source community for inspiration and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/MoviePicker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/MoviePicker/discussions)
- **Email**: your.email@example.com

---

**Built with ❤️ for movie lovers everywhere**