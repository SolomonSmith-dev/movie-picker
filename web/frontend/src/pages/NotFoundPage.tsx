import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, Search, ArrowLeft } from 'lucide-react'

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* 404 Animation */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="text-8xl mb-6"
          >
            🎬
          </motion.div>
          
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-6xl font-bold mb-4"
          >
            404
          </motion.h1>
          
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-2xl font-semibold mb-4"
          >
            Page Not Found
          </motion.h2>
          
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="text-white/60 mb-8"
          >
            Oops! The page you're looking for doesn't exist. 
            Maybe it got lost in the director's cut?
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="space-y-4"
          >
            <Link
              to="/"
              className="btn-primary inline-flex items-center gap-2"
            >
              <Home size={16} />
              Go Home
            </Link>
            
            <div className="flex gap-4 justify-center">
              <Link
                to="/movies"
                className="btn-secondary inline-flex items-center gap-2"
              >
                <Search size={16} />
                Browse Movies
              </Link>
              
              <button
                onClick={() => window.history.back()}
                className="btn-secondary inline-flex items-center gap-2"
              >
                <ArrowLeft size={16} />
                Go Back
              </button>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default NotFoundPage 