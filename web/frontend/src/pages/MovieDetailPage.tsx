import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { Star, Clock, Calendar, Heart, Play, ArrowLeft, Share2, Bookmark } from 'lucide-react'
import { moviesApi, recommendationsApi } from '@/services/api'
import MovieCard from '@/components/MovieCard'
import { Movie } from '@/types'
import { formatYear, formatRuntime } from '@/utils/format'
import toast from 'react-hot-toast'

const MovieDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const movieId = parseInt(id!)

  const { data: movie, isLoading, error } = useQuery(
    ['movie', movieId],
    () => moviesApi.getMovie(movieId),
    {
      enabled: !!movieId,
    }
  )

  const { data: similarMovies } = useQuery(
    ['similarMovies', movieId],
    () => recommendationsApi.getSimilarMovies(1, movieId, 5),
    {
      enabled: !!movieId,
    }
  )

  const handleWatch = () => {
    toast.success(`Added "${movie?.title}" to watch list!`)
    // TODO: Implement watch functionality
  }

  const handleFavorite = () => {
    toast.success(`Added "${movie?.title}" to favorites!`)
    // TODO: Implement favorite functionality
  }

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: movie?.title,
        text: `Check out "${movie?.title}" on MoviePicker!`,
        url: window.location.href,
      })
    } else {
      navigator.clipboard.writeText(window.location.href)
      toast.success('Link copied to clipboard!')
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-white/60">Loading movie details...</p>
        </div>
      </div>
    )
  }

  if (error || !movie) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h3 className="text-xl font-semibold mb-2">Movie not found</h3>
          <p className="text-white/60 mb-4">The movie you're looking for doesn't exist.</p>
          <Link to="/movies" className="btn-primary">
            Browse Movies
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-bg">
      {/* Back Button */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <Link
          to="/movies"
          className="inline-flex items-center gap-2 text-white/70 hover:text-white transition-colors mb-8"
        >
          <ArrowLeft size={20} />
          Back to Movies
        </Link>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-8"
        >
          {/* Movie Poster */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              {movie.poster_url ? (
                <img
                  src={movie.poster_url}
                  alt={movie.title}
                  className="w-full rounded-lg shadow-2xl"
                />
              ) : (
                <div className="w-full aspect-[2/3] bg-movie-accent rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-6xl mb-2">🎬</div>
                    <div className="text-white/60">No Poster</div>
                  </div>
                </div>
              )}
            </motion.div>
          </div>

          {/* Movie Details */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h1 className="text-4xl font-bold mb-4">{movie.title}</h1>
              
              {/* Meta Info */}
              <div className="flex flex-wrap items-center gap-4 mb-6 text-white/70">
                {movie.year && (
                  <div className="flex items-center gap-1">
                    <Calendar size={16} />
                    <span>{formatYear(movie.year)}</span>
                  </div>
                )}
                {movie.runtime && (
                  <div className="flex items-center gap-1">
                    <Clock size={16} />
                    <span>{formatRuntime(movie.runtime)}</span>
                  </div>
                )}
                {movie.rating && (
                  <div className="flex items-center gap-1">
                    <Star size={16} className="text-yellow-400 fill-current" />
                    <span>{movie.rating.toFixed(1)}/10</span>
                  </div>
                )}
              </div>

              {/* Director */}
              {movie.director && (
                <div className="mb-4">
                  <span className="text-white/60">Director: </span>
                  <span className="text-white">{movie.director}</span>
                </div>
              )}

              {/* Genres */}
              {movie.genres && (
                <div className="mb-6">
                  <span className="text-white/60">Genres: </span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {movie.genres.split(',').map((genre, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-primary-500/20 text-primary-300 text-sm rounded-full"
                      >
                        {genre.trim()}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Cast */}
              {movie.cast && (
                <div className="mb-6">
                  <span className="text-white/60">Cast: </span>
                  <span className="text-white">{movie.cast}</span>
                </div>
              )}

              {/* Overview */}
              {movie.overview && (
                <div className="mb-8">
                  <h3 className="text-lg font-semibold mb-2">Overview</h3>
                  <p className="text-white/80 leading-relaxed">{movie.overview}</p>
                </div>
              )}

              {/* Actions */}
              <div className="flex flex-wrap gap-4 mb-8">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleWatch}
                  className="btn-primary flex items-center gap-2"
                >
                  <Play size={16} />
                  Add to Watch List
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleFavorite}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Heart size={16} />
                  Add to Favorites
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleShare}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Share2 size={16} />
                  Share
                </motion.button>
              </div>

              {/* Additional Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {movie.language && (
                  <div>
                    <span className="text-white/60">Language: </span>
                    <span className="text-white">{movie.language}</span>
                  </div>
                )}
                {movie.country && (
                  <div>
                    <span className="text-white/60">Country: </span>
                    <span className="text-white">{movie.country}</span>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Similar Movies */}
        {similarMovies && similarMovies.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-16"
          >
            <h2 className="text-2xl font-bold mb-6">Similar Movies</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {similarMovies.map((similarMovie) => (
                <MovieCard
                  key={similarMovie.id}
                  movie={similarMovie}
                  onWatch={handleWatch}
                  onFavorite={handleFavorite}
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default MovieDetailPage 