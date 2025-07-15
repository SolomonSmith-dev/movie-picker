export interface Movie {
  id: number
  title: string
  director?: string
  year?: number
  genres?: string
  cast?: string
  tmdb_id?: number
  poster_url?: string
  overview?: string
  rating?: number
  runtime?: number
  language?: string
  country?: string
}

export interface MovieListResponse {
  movies: Movie[]
  total: number
  page: number
  per_page: number
}

export interface MovieFilters {
  search?: string
  genre?: string
  year_min?: number
  year_max?: number
  rating_min?: number
  rating_max?: number
  order_by?: string
  order_direction?: string
}

export interface MovieStats {
  total_movies: number
  year_range?: {
    min: number
    max: number
  }
  rating_range?: {
    min: number
    max: number
    average: number
  }
  runtime_range?: {
    min: number
    max: number
    average: number
  }
  available_genres?: string[]
  available_languages?: string[]
}

export interface User {
  id: number
  username: string
  email?: string
  created_at: string
}

export interface WatchHistoryEntry {
  movie: Movie
  watched_at: string
  rating?: number
}

export interface Recommendation {
  category: string
  movies: Movie[]
} 