# MoviePicker Frontend

A modern React frontend for the MoviePicker application, built with TypeScript, Tailwind CSS, and Framer Motion.

## 🚀 Features

- **Modern UI/UX** - Beautiful, responsive design with smooth animations
- **Movie Discovery** - Browse, search, and filter movies
- **Movie Details** - Comprehensive movie information with similar recommendations
- **User Profiles** - Watch history, preferences, and statistics
- **Settings** - Customizable user preferences and app settings
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **React Query** - Data fetching and caching
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Toast notifications

## 📦 Installation

1. **Navigate to the frontend directory**
   ```bash
   cd web/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx      # Navigation header
│   ├── MovieCard.tsx   # Movie card component
│   └── MovieGrid.tsx   # Movie grid layout
├── pages/              # Page components
│   ├── HomePage.tsx    # Landing page
│   ├── MoviesPage.tsx  # Movie browsing
│   ├── MovieDetailPage.tsx # Movie details
│   ├── ProfilePage.tsx # User profile
│   ├── SettingsPage.tsx # App settings
│   └── NotFoundPage.tsx # 404 page
├── services/           # API services
│   └── api.ts         # API client functions
├── types/              # TypeScript definitions
│   └── index.ts       # Type definitions
├── utils/              # Utility functions
│   └── format.ts      # Formatting utilities
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## 🎨 Design System

### Colors
- **Primary**: Orange gradient (`#ed7a1a` to `#f1953d`)
- **Background**: Dark movie theme (`#0f0f23`, `#1a1a2e`)
- **Accent**: Blue accent (`#16213e`)

### Components
- **Glass Effect**: Semi-transparent backgrounds with blur
- **Movie Cards**: Hover animations and poster display
- **Buttons**: Primary and secondary button styles
- **Forms**: Consistent input styling

### Animations
- **Page Transitions**: Smooth fade-in animations
- **Hover Effects**: Scale and color transitions
- **Loading States**: Spinner animations
- **Toast Notifications**: Slide-in notifications

## 🔌 API Integration

The frontend connects to the FastAPI backend through:

- **Movies API**: Browse, search, and get movie details
- **Users API**: User profiles and preferences
- **Recommendations API**: Personalized movie suggestions
- **Watch History API**: Track watched movies

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet**: Responsive grid layouts
- **Desktop**: Full-featured desktop experience
- **Touch Friendly**: Large touch targets and gestures

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

### Deploy to Netlify
```bash
npm run build
# Upload dist/ folder to Netlify
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=MoviePicker
```

### Vite Configuration
The Vite config includes:
- React plugin
- TypeScript support
- Path aliases (`@/` for `src/`)
- API proxy for development
- Build optimization

## 🎯 Future Enhancements

- [ ] User authentication and login
- [ ] Watchlist and favorites functionality
- [ ] Movie night planning features
- [ ] Advanced filtering and sorting
- [ ] Offline support with service workers
- [ ] Push notifications
- [ ] Dark/light theme toggle
- [ ] Internationalization (i18n)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 