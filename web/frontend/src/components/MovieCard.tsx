import React from 'react'
import { motion } from 'framer-motion'
import { Star, Clock, Calendar, Heart, Play } from 'lucide-react'
import { Movie } from '@/types'
import { formatYear } from '@/utils/format'

interface MovieCardProps {
  movie: Movie
  onWatch?: (movie: Movie) => void
  onFavorite?: (movie: Movie) => void
  showActions?: boolean
}

const MovieCard: React.FC<MovieCardProps> = ({ 
  movie, 
  onWatch, 
  onFavorite, 
  showActions = true 
}) => {
  const handleWatch = () => {
    onWatch?.(movie)
  }

  const handleFavorite = () => {
    onFavorite?.(movie)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="movie-card group"
    >
      {/* Poster */}
      <div className="relative overflow-hidden">
        {movie.poster_url ? (
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="w-full h-80 object-cover transition-transform duration-300 group-hover:scale-110"
          />
        ) : (
          <div className="w-full h-80 bg-movie-accent flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl mb-2">🎬</div>
              <div className="text-white/60 text-sm">No Poster</div>
            </div>
          </div>
        )}
        
        {/* Overlay with actions */}
        {showActions && (
          <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4">
            <button
              onClick={handleWatch}
              className="btn-primary flex items-center gap-2"
            >
              <Play size={16} />
              Watch
            </button>
            <button
              onClick={handleFavorite}
              className="btn-secondary flex items-center gap-2"
            >
              <Heart size={16} />
              Favorite
            </button>
          </div>
        )}
      </div>

      {/* Movie Info */}
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2 group-hover:text-primary-400 transition-colors">
          {movie.title}
        </h3>
        
        <div className="space-y-2 text-sm text-white/70">
          {/* Director */}
          {movie.director && (
            <div className="flex items-center gap-1">
              <span className="font-medium">Director:</span>
              <span>{movie.director}</span>
            </div>
          )}
          
          {/* Year */}
          {movie.year && (
            <div className="flex items-center gap-1">
              <Calendar size={14} />
              <span>{formatYear(movie.year)}</span>
            </div>
          )}
          
          {/* Rating */}
          {movie.rating && (
            <div className="flex items-center gap-1">
              <Star size={14} className="text-yellow-400 fill-current" />
              <span>{movie.rating.toFixed(1)}/10</span>
            </div>
          )}
          
          {/* Runtime */}
          {movie.runtime && (
            <div className="flex items-center gap-1">
              <Clock size={14} />
              <span>{movie.runtime} min</span>
            </div>
          )}
          
          {/* Genres */}
          {movie.genres && (
            <div className="flex flex-wrap gap-1 mt-2">
              {movie.genres.split(',').slice(0, 3).map((genre, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-primary-500/20 text-primary-300 text-xs rounded-full"
                >
                  {genre.trim()}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

export default MovieCard 