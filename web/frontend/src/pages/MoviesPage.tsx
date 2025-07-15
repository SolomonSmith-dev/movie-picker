import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { Search, Filter, Grid, List, ChevronLeft, ChevronRight } from 'lucide-react'
import { moviesApi } from '@/services/api'
import MovieGrid from '@/components/MovieGrid'
import { Movie, MovieFilters } from '@/types'
import toast from 'react-hot-toast'

const MoviesPage: React.FC = () => {
  const [filters, setFilters] = useState<MovieFilters>({})
  const [searchQuery, setSearchQuery] = useState('')
  const [page, setPage] = useState(1)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

  const { data: moviesData, isLoading, error } = useQuery(
    ['movies', filters, searchQuery, page],
    () => moviesApi.getMovies(filters, page, 20),
    {
      keepPreviousData: true,
    }
  )

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setFilters(prev => ({ ...prev, search: searchQuery }))
    setPage(1)
  }

  const handleFilterChange = (newFilters: Partial<MovieFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }))
    setPage(1)
  }

  const handleWatch = (movie: Movie) => {
    toast.success(`Added "${movie.title}" to watch list!`)
    // TODO: Implement watch functionality
  }

  const handleFavorite = (movie: Movie) => {
    toast.success(`Added "${movie.title}" to favorites!`)
    // TODO: Implement favorite functionality
  }

  const totalPages = moviesData ? Math.ceil(moviesData.total / 20) : 0

  return (
    <div className="min-h-screen gradient-bg py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-4">🎬 Browse Movies</h1>
          <p className="text-white/60">Discover thousands of movies from around the world</p>
        </motion.div>

        {/* Search and Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-effect p-6 rounded-lg mb-8"
        >
          <div className="flex flex-col lg:flex-row gap-6">
            {/* Search */}
            <div className="flex-1">
              <form onSubmit={handleSearch} className="relative">
                <input
                  type="text"
                  placeholder="Search movies by title, director, or actor..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input-field w-full pr-12"
                />
                <button
                  type="submit"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white"
                >
                  <Search size={20} />
                </button>
              </form>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-lg transition-colors ${
                  viewMode === 'grid' ? 'bg-primary-500 text-white' : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                <Grid size={20} />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-lg transition-colors ${
                  viewMode === 'list' ? 'bg-primary-500 text-white' : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                <List size={20} />
              </button>
            </div>
          </div>

          {/* Quick Filters */}
          <div className="mt-6 flex flex-wrap gap-2">
            {[
              { label: 'All', value: '' },
              { label: 'Action', value: 'Action' },
              { label: 'Drama', value: 'Drama' },
              { label: 'Comedy', value: 'Comedy' },
              { label: 'Sci-Fi', value: 'Sci-Fi' },
              { label: 'Horror', value: 'Horror' },
            ].map((filter) => (
              <button
                key={filter.value}
                onClick={() => handleFilterChange({ genre: filter.value || undefined })}
                className={`px-4 py-2 rounded-full text-sm transition-colors ${
                  filters.genre === filter.value
                    ? 'bg-primary-500 text-white'
                    : 'bg-white/10 text-white/70 hover:text-white hover:bg-white/20'
                }`}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Movies Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <MovieGrid
            movies={moviesData?.movies || []}
            loading={isLoading}
            error={error?.message}
            onWatch={handleWatch}
            onFavorite={handleFavorite}
          />
        </motion.div>

        {/* Pagination */}
        {totalPages > 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex items-center justify-center gap-4 mt-8"
          >
            <button
              onClick={() => setPage(prev => Math.max(1, prev - 1))}
              disabled={page === 1}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <ChevronLeft size={16} />
              Previous
            </button>

            <div className="flex items-center gap-2">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = i + 1
                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`w-10 h-10 rounded-lg transition-colors ${
                      page === pageNum
                        ? 'bg-primary-500 text-white'
                        : 'bg-white/10 text-white/70 hover:text-white hover:bg-white/20'
                    }`}
                  >
                    {pageNum}
                  </button>
                )
              })}
            </div>

            <button
              onClick={() => setPage(prev => Math.min(totalPages, prev + 1))}
              disabled={page === totalPages}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              Next
              <ChevronRight size={16} />
            </button>
          </motion.div>
        )}

        {/* Results Info */}
        {moviesData && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-center mt-8 text-white/60"
          >
            Showing {((page - 1) * 20) + 1} to {Math.min(page * 20, moviesData.total)} of {moviesData.total} movies
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default MoviesPage 