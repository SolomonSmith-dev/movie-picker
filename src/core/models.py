"""Database models for MoviePicker application."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Movie(Base):
    """Movie model representing a movie in the database."""
    
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    director = Column(String(255))
    year = Column(Integer, index=True)
    genres = Column(Text)  # Comma-separated genres
    cast = Column(Text)    # Comma-separated cast
    tmdb_id = Column(Integer, unique=True, index=True)
    poster_url = Column(String(500))
    overview = Column(Text)
    rating = Column(Float)
    runtime = Column(Integer)
    language = Column(String(10))
    country = Column(String(100))
    
    # Relationships
    watch_history = relationship("WatchHistory", back_populates="movie")
    user_ratings = relationship("UserRating", back_populates="movie")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    """User model for user management."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    preferences = Column(Text)  # JSON string of user preferences
    
    # Relationships
    watch_history = relationship("WatchHistory", back_populates="user")
    user_ratings = relationship("UserRating", back_populates="user")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WatchHistory(Base):
    """Watch history model to track when users watch movies."""
    
    __tablename__ = "watch_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    watched_at = Column(DateTime, default=datetime.utcnow)
    is_favorite = Column(Boolean, default=False)
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")


class UserRating(Base):
    """User ratings for movies."""
    
    __tablename__ = "user_ratings"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-10 scale
    review = Column(Text)
    rated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_ratings")
    movie = relationship("Movie", back_populates="user_ratings")


class MovieNight(Base):
    """Movie night model for group watching sessions."""
    
    __tablename__ = "movie_nights"
    
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")  # scheduled, active, completed, cancelled
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MovieNightVote(Base):
    """Votes for movies in a movie night."""
    
    __tablename__ = "movie_night_votes"
    
    id = Column(Integer, primary_key=True)
    movie_night_id = Column(Integer, ForeignKey("movie_nights.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    voted_at = Column(DateTime, default=datetime.utcnow) 