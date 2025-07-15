import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from '@/components/Header'
import HomePage from '@/pages/HomePage'
import MoviesPage from '@/pages/MoviesPage'
import MovieDetailPage from '@/pages/MovieDetailPage'
import ProfilePage from '@/pages/ProfilePage'
import SettingsPage from '@/pages/SettingsPage'
import NotFoundPage from '@/pages/NotFoundPage'

const App: React.FC = () => {
  const handleSearch = (query: string) => {
    // TODO: Implement search functionality
    console.log('Search query:', query)
  }

  return (
    <div className="min-h-screen bg-movie-dark">
      <Header onSearch={handleSearch} />
      
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/movies" element={<MoviesPage />} />
          <Route path="/movies/:id" element={<MovieDetailPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App 