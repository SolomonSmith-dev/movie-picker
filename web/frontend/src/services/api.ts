import axios from 'axios'
import { Movie, MovieListResponse, MovieFilters, MovieStats, User, WatchHistoryEntry, Recommendation } from '@/types'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Movies API
export const moviesApi = {
  // Get movies with filters
  getMovies: async (filters: MovieFilters = {}, page = 1, perPage = 20): Promise<MovieListResponse> => {
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: perPage.toString(),
      ...filters,
    })
    
    const response = await api.get(`/movies/?${params}`)
    return response.data
  },

  // Get movie by ID
  getMovie: async (id: number): Promise<Movie> => {
    const response = await api.get(`/movies/${id}`)
    return response.data
  },

  // Get movie of the day
  getMovieOfTheDay: async (): Promise<Movie> => {
    const response = await api.get('/movies/movie-of-the-day')
    return response.data
  },

  // Pick random movie
  pickRandomMovie: async (excludeWatched = true): Promise<Movie> => {
    const response = await api.get('/movies/random/pick', {
      params: { exclude_watched: excludeWatched }
    })
    return response.data
  },

  // Get top rated movies
  getTopRated: async (limit = 10): Promise<Movie[]> => {
    const response = await api.get('/movies/top-rated', {
      params: { limit }
    })
    return response.data
  },

  // Get recent movies
  getRecent: async (limit = 10): Promise<Movie[]> => {
    const response = await api.get('/movies/recent', {
      params: { limit }
    })
    return response.data
  },

  // Get movie statistics
  getStats: async (): Promise<MovieStats> => {
    const response = await api.get('/movies/stats')
    return response.data
  },
}

// Users API
export const usersApi = {
  // Get all users
  getUsers: async (): Promise<User[]> => {
    const response = await api.get('/users/')
    return response.data
  },

  // Get user by ID
  getUser: async (id: number): Promise<User> => {
    const response = await api.get(`/users/${id}`)
    return response.data
  },

  // Create user
  createUser: async (userData: { username: string; email?: string }): Promise<User> => {
    const response = await api.post('/users/', userData)
    return response.data
  },
}

// Recommendations API
export const recommendationsApi = {
  // Get user recommendations
  getUserRecommendations: async (userId = 1, limit = 10): Promise<Recommendation[]> => {
    const response = await api.get(`/recommendations/${userId}`, {
      params: { limit }
    })
    return response.data
  },

  // Get similar movies
  getSimilarMovies: async (userId = 1, movieId: number, limit = 5): Promise<Movie[]> => {
    const response = await api.get(`/recommendations/${userId}/similar/${movieId}`, {
      params: { limit }
    })
    return response.data
  },

  // Get user preferences
  getUserPreferences: async (userId = 1): Promise<any> => {
    const response = await api.get(`/recommendations/${userId}/preferences`)
    return response.data
  },
}

// Watch history API (to be implemented in backend)
export const watchHistoryApi = {
  // Get user watch history
  getWatchHistory: async (userId = 1, limit = 50): Promise<WatchHistoryEntry[]> => {
    // This endpoint needs to be implemented in the backend
    const response = await api.get(`/users/${userId}/watch-history`, {
      params: { limit }
    })
    return response.data
  },

  // Mark movie as watched
  markAsWatched: async (userId = 1, movieId: number, rating?: number): Promise<void> => {
    // This endpoint needs to be implemented in the backend
    await api.post(`/users/${userId}/watch-history`, {
      movie_id: movieId,
      rating
    })
  },
}

export default api 