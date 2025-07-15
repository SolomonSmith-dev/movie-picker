import React from 'react'
import { useQuery } from 'react-query'
import { motion } from 'framer-motion'
import { User, Clock, Star, Heart, Settings, Calendar, TrendingUp } from 'lucide-react'
import { usersApi, watchHistoryApi, recommendationsApi } from '@/services/api'
import MovieCard from '@/components/MovieCard'
import { Movie } from '@/types'
import { formatDate } from '@/utils/format'
import toast from 'react-hot-toast'

const ProfilePage: React.FC = () => {
  const userId = 1 // TODO: Get from auth context

  const { data: user } = useQuery(
    ['user', userId],
    () => usersApi.getUser(userId),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  )

  const { data: watchHistory } = useQuery(
    ['watchHistory', userId],
    () => watchHistoryApi.getWatchHistory(userId, 20),
    {
      staleTime: 60 * 1000, // 1 minute
    }
  )

  const { data: userPreferences } = useQuery(
    ['userPreferences', userId],
    () => recommendationsApi.getUserPreferences(userId),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
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
    <div className="min-h-screen gradient-bg py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-effect p-8 rounded-lg mb-8"
        >
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center">
              <User size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold mb-2">
                {user?.username || 'Movie Lover'}
              </h1>
              <p className="text-white/60">
                Member since {user?.created_at ? formatDate(user.created_at) : 'recently'}
              </p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-1"
          >
            <div className="glass-effect p-6 rounded-lg mb-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <TrendingUp size={20} />
                Your Stats
              </h2>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-white/60">Movies Watched</span>
                  <span className="text-2xl font-bold text-primary-500">
                    {watchHistory?.length || 0}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-white/60">Average Rating</span>
                  <span className="text-2xl font-bold text-primary-500">
                    {userPreferences?.preferences?.average_rating || 'N/A'}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-white/60">Favorite Genre</span>
                  <span className="text-lg font-semibold">
                    {userPreferences?.preferences?.favorite_genres?.[0] || 'None yet'}
                  </span>
                </div>
              </div>
            </div>

            {/* Preferences */}
            {userPreferences?.preferences && (
              <div className="glass-effect p-6 rounded-lg">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Settings size={20} />
                  Your Preferences
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <span className="text-white/60 text-sm">Favorite Genres</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {userPreferences.preferences.favorite_genres?.slice(0, 5).map((genre, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-primary-500/20 text-primary-300 text-xs rounded-full"
                        >
                          {genre}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <span className="text-white/60 text-sm">Total Rated</span>
                    <p className="text-lg font-semibold">
                      {userPreferences.preferences.total_rated || 0} movies
                    </p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>

          {/* Watch History */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="glass-effect p-6 rounded-lg">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Clock size={20} />
                Recent Watch History
              </h2>
              
              {watchHistory && watchHistory.length > 0 ? (
                <div className="space-y-4">
                  {watchHistory.slice(0, 10).map((entry, index) => (
                    <motion.div
                      key={entry.movie.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.3 + index * 0.1 }}
                      className="flex items-center gap-4 p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                    >
                      {entry.movie.poster_url ? (
                        <img
                          src={entry.movie.poster_url}
                          alt={entry.movie.title}
                          className="w-16 h-24 object-cover rounded"
                        />
                      ) : (
                        <div className="w-16 h-24 bg-movie-accent rounded flex items-center justify-center">
                          <div className="text-2xl">🎬</div>
                        </div>
                      )}
                      
                      <div className="flex-1">
                        <h3 className="font-semibold">{entry.movie.title}</h3>
                        <p className="text-white/60 text-sm">
                          Watched {formatDate(entry.watched_at)}
                        </p>
                        {entry.rating && (
                          <div className="flex items-center gap-1 mt-1">
                            <Star size={14} className="text-yellow-400 fill-current" />
                            <span className="text-sm">{entry.rating}/10</span>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="text-6xl mb-4">📺</div>
                  <h3 className="text-lg font-semibold mb-2">No watch history yet</h3>
                  <p className="text-white/60">Start watching movies to see them here!</p>
                </div>
              )}
            </div>
          </motion.div>
        </div>

        {/* Favorite Movies Grid */}
        {watchHistory && watchHistory.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-8"
          >
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Heart size={24} />
              Your Watched Movies
            </h2>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {watchHistory.slice(0, 10).map((entry) => (
                <MovieCard
                  key={entry.movie.id}
                  movie={entry.movie}
                  onWatch={handleWatch}
                  onFavorite={handleFavorite}
                  showActions={false}
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default ProfilePage 