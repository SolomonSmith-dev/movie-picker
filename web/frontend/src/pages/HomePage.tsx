import React from 'react'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { Play, Star, Clock, Calendar, Sparkles, TrendingUp, Clock as ClockIcon } from 'lucide-react'
import { moviesApi } from '@/services/api'
import MovieCard from '@/components/MovieCard'
import MovieGrid from '@/components/MovieGrid'
import { Movie } from '@/types'
import toast from 'react-hot-toast'

const HomePage: React.FC = () => {
  // Fetch movie of the day
  const { data: movieOfTheDay, isLoading: loadingMovieOfTheDay } = useQuery(
    'movieOfTheDay',
    moviesApi.getMovieOfTheDay,
    {
      staleTime: 24 * 60 * 60 * 1000, // 24 hours
    }
  )

  // Fetch top rated movies
  const { data: topRatedMovies, isLoading: loadingTopRated } = useQuery(
    'topRatedMovies',
    () => moviesApi.getTopRated(8),
    {
      staleTime: 60 * 60 * 1000, // 1 hour
    }
  )

  // Fetch recent movies
  const { data: recentMovies, isLoading: loadingRecent } = useQuery(
    'recentMovies',
    () => moviesApi.getRecent(8),
    {
      staleTime: 60 * 60 * 1000, // 1 hour
    }
  )

  const handleWatch = (movie: Movie) => {
    toast.success(`Added "${movie.title}" to watch list!`)
    // TODO: Implement watch functionality
  }

  const handleFavorite = (movie: Movie) => {
    toast.success(`Added "${movie.title}" to favorites!`)
    // TODO: Implement favorite functionality
  }

  return (
    <div className="min-h-screen gradient-bg">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">Discover Your Next</span>
              <br />
              <span className="text-primary-500">Favorite Movie</span>
            </h1>
            <p className="text-xl text-white/70 mb-8 max-w-3xl mx-auto">
              Get AI-powered movie recommendations based on your taste. 
              Explore thousands of films and find your perfect match.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary text-lg px-8 py-4 flex items-center justify-center gap-2"
              >
                <Play size={20} />
                Start Exploring
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-secondary text-lg px-8 py-4 flex items-center justify-center gap-2"
              >
                <Sparkles size={20} />
                Get Recommendations
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Movie of the Day */}
      {movieOfTheDay && (
        <section className="py-16 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl font-bold mb-2">🎬 Movie of the Day</h2>
              <p className="text-white/60">Today's featured pick just for you</p>
            </motion.div>

            <div className="flex justify-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="max-w-md"
              >
                <MovieCard
                  movie={movieOfTheDay}
                  onWatch={handleWatch}
                  onFavorite={handleFavorite}
                />
              </motion.div>
            </div>
          </div>
        </section>
      )}

      {/* Top Rated Movies */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex items-center gap-3 mb-8"
          >
            <TrendingUp className="text-primary-500" size={24} />
            <h2 className="text-3xl font-bold">Top Rated Movies</h2>
          </motion.div>

          <MovieGrid
            movies={topRatedMovies || []}
            loading={loadingTopRated}
            onWatch={handleWatch}
            onFavorite={handleFavorite}
          />
        </div>
      </section>

      {/* Recent Movies */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="flex items-center gap-3 mb-8"
          >
            <ClockIcon className="text-primary-500" size={24} />
            <h2 className="text-3xl font-bold">Recent Releases</h2>
          </motion.div>

          <MovieGrid
            movies={recentMovies || []}
            loading={loadingRecent}
            onWatch={handleWatch}
            onFavorite={handleFavorite}
          />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Why Choose MoviePicker?</h2>
            <p className="text-white/60 max-w-2xl mx-auto">
              Our AI-powered recommendation engine learns your preferences and suggests 
              movies you'll actually love.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Sparkles,
                title: 'Smart Recommendations',
                description: 'AI-powered suggestions based on your watch history and preferences',
              },
              {
                icon: Star,
                title: 'Curated Collections',
                description: 'Hand-picked movies from critics and movie enthusiasts',
              },
              {
                icon: Clock,
                title: 'Movie of the Day',
                description: 'Get a fresh movie recommendation every single day',
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.7 + index * 0.1 }}
                className="glass-effect p-6 rounded-lg text-center"
              >
                <feature.icon className="w-12 h-12 text-primary-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage 