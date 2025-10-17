# CineMatch - Advanced Movie Recommendation System

A modern, feature-rich movie recommendation web application built with Flask and enhanced with multiple user-centric features.

## New Features Added

### Multi-Section Navigation
- **Recommendations**: Get personalized movie suggestions based on a movie you like
- **Search**: Find movies by title with intelligent partial matching
- **Popular**: Browse randomly selected popular movies from the database
- **Genres**: Explore movies by specific genres
- **My Lists**: Manage your personal favorites and watchlist

### Enhanced User Experience
- **Interactive Movie Cards**: Hover effects, modern styling, and intuitive interactions
- **Detailed Movie Modals**: Click any movie card to see comprehensive details
- **Star Rating System**: Rate movies from 1-5 stars with persistent storage
- **Favorites System**: Add movies to your favorites list with heart icon
- **Watchlist Feature**: Bookmark movies to watch later
- **Local Storage**: All user preferences saved in browser

### Modern UI/UX Design
- **Responsive Design**: Fully optimized for desktop, tablet, and mobile
- **Modern Animations**: Smooth transitions and hover effects
- **Gradient Theme**: Beautiful purple gradient background
- **Glass Morphism**: Frosted glass effect on cards and containers
- **Font Awesome Icons**: Professional iconography throughout
- **Loading States**: Elegant loading spinners and animations

### Advanced Functionality
- **Multi-endpoint API**: Separate endpoints for different content types
- **Error Handling**: Comprehensive error messages and fallbacks
- **Genre Management**: Dynamic genre loading and filtering
- **Statistics Ready**: Backend prepared for analytics dashboard
- **Organized Code**: Separated CSS into external file for maintainability

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install flask flask-cors pandas joblib
   ```

2. **Ensure Data Files are Present**:
   - `movies_with_posters.csv` - Movie dataset with poster URLs
   - `cosine_similarity_matrix.pkl` - Pre-computed similarity matrix

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Open in Browser**:
   Navigate to `http://localhost:5000`

## How to Use

### Getting Recommendations
1. Click on the "Recommendations" tab
2. Enter a movie title you enjoyed
3. Click "Get Recommendations" to see similar movies

### Searching Movies
1. Switch to the "Search" tab
2. Enter any movie title or partial title
3. Browse through the search results

### Exploring Popular Movies
1. Go to the "Popular" tab
2. Click "Load Popular Movies" to see random selections

### Browsing by Genre
1. Select the "Genres" tab
2. Choose a genre from the dropdown
3. Click "Browse Genre" to see movies in that category

### Managing Your Lists
1. **Adding to Favorites/Watchlist**:
   - Hover over any movie card
- Click the heart icon for favorites
- Click the bookmark icon for watchlist

2. **Rating Movies**:
   - Click on the stars below any movie title
   - Your ratings are saved automatically

3. **Viewing Your Lists**:
   - Go to "My Lists" tab
   - Switch between "Favorites" and "Watchlist"
   - Remove items as needed

### Viewing Movie Details
- Click anywhere on a movie card (except icons)
- A modal will open with full movie information
- Add to lists or rate directly from the modal

## 🔧 Technical Features

### Backend (Flask)
- **Multiple API Endpoints**:
  - `/recommend` - Get movie recommendations
  - `/search` - Search movies by title
  - `/popular` - Get random popular movies
  - `/genres` - List all available genres
  - `/genre/<name>` - Get movies by genre
  - `/stats` - Database statistics (ready for implementation)

### Frontend (JavaScript)
- **Modern ES6+ JavaScript**
- **Async/Await for API calls**
- **Local Storage for user data**
- **Responsive event handling**
- **Dynamic DOM manipulation**
- **Modal system for detailed views**

### Styling (CSS)
- **CSS Grid and Flexbox layouts**
- **CSS Variables for consistent theming**
- **Media queries for responsiveness**
- **CSS animations and transitions**
- **Backdrop-filter for glass effects**

## Mobile Responsive
- Optimized layouts for all screen sizes
- Touch-friendly interface elements
- Collapsible navigation on small screens
- Readable text and appropriately sized buttons

## Data Persistence
- User ratings stored in localStorage
- Favorites list persisted across sessions  
- Watchlist maintained in browser storage
- No account creation required

## Future Enhancement Ideas
- User authentication system
- Social features (share lists, reviews)
- Advanced filtering (year, rating, etc.)
- Movie trailers integration
- Recommendation algorithm improvements
- Export/import user lists
- Statistics dashboard implementation

## 📁 Project Structure
```
Movie recommender/
├── app.py                 # Flask backend with all endpoints
├── templates/
│   └── index.html        # Complete frontend application
├── static/
│   └── style.css         # Organized styling
├── movies_with_posters.csv
├── cosine_similarity_matrix.pkl
└── README.md
```

## Technologies Used
- **Backend**: Python, Flask, Pandas, Joblib
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: CSS Grid, Flexbox, CSS Animations
- **Icons**: Font Awesome 6
- **Data Storage**: LocalStorage for user preferences

## Performance Optimizations
- Efficient API calls with proper error handling
- Lazy loading of genre data
- Optimized CSS with modern properties
- Responsive images with fallbacks
- Minimal DOM manipulation for smooth performance

---

**Enjoy exploring movies with CineMatch!**
