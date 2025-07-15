import React from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import MovieCard from './MovieCard'
import { Movie } from '@/types'

interface MovieGridProps {
  movies: Movie[]
  loading?: boolean
  error?: string
  onWatch?: (movie: Movie) => void
  onFavorite?: (movie: Movie) => void
  showActions?: boolean
}

const MovieGrid: React.FC<MovieGridProps> = ({
  movies,
  loading = false,
  error,
  onWatch,
  onFavorite,
  showActions = true,
}) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-white/60">Loading movies...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h3 className="text-xl font-semibold mb-2">Oops! Something went wrong</h3>
          <p className="text-white/60">{error}</p>
        </div>
      </div>
    )
  }

  if (!movies.length) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="text-6xl mb-4">🎬</div>
          <h3 className="text-xl font-semibold mb-2">No movies found</h3>
          <p className="text-white/60">Try adjusting your filters or search terms</p>
        </div>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6"
    >
      {movies.map((movie, index) => (
        <motion.div
          key={movie.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
        >
          <MovieCard
            movie={movie}
            onWatch={onWatch}
            onFavorite={onFavorite}
            showActions={showActions}
          />
        </motion.div>
      ))}
    </motion.div>
  )
}

export default MovieGrid 