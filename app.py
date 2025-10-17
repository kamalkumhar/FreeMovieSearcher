from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from flask_cors import CORS  # Import Flask-CORS
import pandas as pd
import joblib
import os

app = Flask(__name__, template_folder="templates")  # Specify the folder for HTML templates
CORS(app)  # Enable CORS to allow cross-origin requests

BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"

# Load dataset
try:
    data = pd.read_csv('movies_with_posters.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: movies_with_posters.csv not found.")
    data = None

if data is not None and 'Title' in data.columns:
    data['Title'] = data['Title'].str.strip().str.lower()
else:
    print("Error: Dataset is invalid or missing 'Title' column.")

# Load similarity matrix
try:
    cosine_sim = joblib.load('cosine_similarity_matrix.pkl')
    print("Cosine similarity matrix loaded successfully!")
except FileNotFoundError:
    print("Error: cosine_similarity_matrix.pkl not found.")
    cosine_sim = None

# Get random popular movies
def get_popular_movies(limit=20):
    try:
        if data is None:
            return None
        
        # Sample random movies from the dataset
        popular_movies = data.sample(n=min(limit, len(data)))
        result = popular_movies[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
        
        # Format the data
        result['Title'] = result['Title'].str.title()
        result['poster_path'] = BASE_POSTER_URL + result['poster_path'].fillna('')
        result['overview'] = result['overview'].fillna('No overview available')
        result['Director'] = result['Director'].fillna('Unknown')
        result['Cast'] = result['Cast'].fillna('Unknown')
        result['genres'] = result['genres'].fillna('Unknown')
        
        return result
    except Exception as e:
        print(f"Error getting popular movies: {e}")
        return None

# Search movies by title (Prefix-based for better autocomplete)
def search_movies(query, limit=20):
    try:
        if data is None:
            return None
        
        query_lower = query.strip().lower()
        
        # Priority 1: Movies that START with the query (prefix match)
        starts_with = data[data['Title'].str.startswith(query_lower, na=False)]
        
        # Priority 2: Movies that CONTAIN the query (but don't start with it)
        contains = data[
            data['Title'].str.contains(query_lower, case=False, na=False) & 
            ~data['Title'].str.startswith(query_lower, na=False)
        ]
        
        # Combine: prefix matches first, then substring matches
        matching_movies = pd.concat([starts_with, contains])
        
        if matching_movies.empty:
            return None
        
        # Limit results
        if len(matching_movies) > limit:
            matching_movies = matching_movies.head(limit)
        
        result = matching_movies[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
        
        # Format the data
        result['Title'] = result['Title'].str.title()
        result['poster_path'] = BASE_POSTER_URL + result['poster_path'].fillna('')
        result['overview'] = result['overview'].fillna('No overview available')
        result['Director'] = result['Director'].fillna('Unknown')
        result['Cast'] = result['Cast'].fillna('Unknown')
        result['genres'] = result['genres'].fillna('Unknown')
        
        return result
    except Exception as e:
        print(f"Error searching movies: {e}")
        return None

# Get movies by genre
def get_movies_by_genre(genre, limit=20):
    try:
        if data is None:
            return None
        
        genre_lower = genre.strip().lower()
        
        # Filter movies by genre
        genre_movies = data[data['genres'].str.contains(genre_lower, case=False, na=False)]
        
        if genre_movies.empty:
            return None
        
        # Limit results
        if len(genre_movies) > limit:
            genre_movies = genre_movies.head(limit)
        
        result = genre_movies[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
        
        # Format the data
        result['Title'] = result['Title'].str.title()
        result['poster_path'] = BASE_POSTER_URL + result['poster_path'].fillna('')
        result['overview'] = result['overview'].fillna('No overview available')
        result['Director'] = result['Director'].fillna('Unknown')
        result['Cast'] = result['Cast'].fillna('Unknown')
        result['genres'] = result['genres'].fillna('Unknown')
        
        return result
    except Exception as e:
        print(f"Error getting movies by genre: {e}")
        return None

# Get available genres
def get_genres():
    try:
        if data is None:
            return []
        
        all_genres = set()
        for genres_str in data['genres'].dropna():
            if isinstance(genres_str, str):
                # Split genres and add to set
                genres = [g.strip() for g in genres_str.split(',')]
                all_genres.update(genres)
        
        return sorted(list(all_genres))
    except Exception as e:
        print(f"Error getting genres: {e}")
        return []

# Recommendation logic (with improved matching)
def recommendations(title):
    try:
        if data is None or cosine_sim is None:
            print("Error: Dataset or cosine similarity matrix not loaded.")
            return None

        # Clean and format the input title
        search_title = title.strip().lower()
        
        # Try multiple matching strategies
        matched_title = None
        
        # Strategy 1: Exact match
        exact_match = data[data['Title'] == search_title]
        if not exact_match.empty:
            matched_title = search_title
            print(f"✓ Exact match found: '{matched_title}'")
        
        # Strategy 2: Prefix match (starts with)
        if matched_title is None:
            starts_with = data[data['Title'].str.startswith(search_title, na=False)]
            if not starts_with.empty:
                matched_title = starts_with.iloc[0]['Title']
                print(f"✓ Prefix match found: '{title}' → '{matched_title}'")
        
        # Strategy 3: Contains match (anywhere in title)
        if matched_title is None:
            contains = data[data['Title'].str.contains(search_title, case=False, na=False, regex=False)]
            if not contains.empty:
                matched_title = contains.iloc[0]['Title']
                print(f"✓ Contains match found: '{title}' → '{matched_title}'")
        
        # Strategy 4: Fuzzy match (remove special chars and try again)
        if matched_title is None:
            import re
            clean_search = re.sub(r'[^\w\s]', '', search_title).strip()
            for movie_title in data['Title']:
                clean_movie = re.sub(r'[^\w\s]', '', str(movie_title)).strip()
                if clean_search in clean_movie or clean_movie in clean_search:
                    matched_title = movie_title
                    print(f"✓ Fuzzy match found: '{title}' → '{matched_title}'")
                    break
        
        # If no match found
        if matched_title is None:
            print(f"✗ Movie title '{title}' not found in dataset after all strategies")
            return None

        # Get the index of the matched movie
        idx = data[data['Title'] == matched_title].index[0]
        
        # Check if index is within cosine similarity matrix bounds
        matrix_size = cosine_sim.shape[0]
        if idx >= matrix_size:
            print(f"⚠️ Warning: Movie index {idx} is out of bounds (matrix size: {matrix_size})")
            print(f"Movie '{matched_title}' is too new or not in the similarity matrix.")
            
            # Fallback: Return movies from same genre
            movie_genres = data.iloc[idx]['genres']
            if pd.notna(movie_genres) and movie_genres != 'Unknown':
                print(f"Fallback: Finding movies with similar genres: {movie_genres}")
                similar_genre_movies = data[
                    (data['genres'].str.contains(movie_genres.split(',')[0].strip(), case=False, na=False)) &
                    (data.index != idx)
                ].head(10)
                
                if not similar_genre_movies.empty:
                    recommended_movies = similar_genre_movies[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
                else:
                    # Last resort: return random popular movies
                    print("Fallback: Returning random popular movies")
                    recommended_movies = data[data.index != idx].sample(n=min(10, len(data)-1))[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
            else:
                # Return random movies as last resort
                recommended_movies = data[data.index != idx].sample(n=min(10, len(data)-1))[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].copy()
        else:
            # Normal recommendation flow
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]  # Get top 10 recommendations
            movie_indices = [i[0] for i in sim_scores]
            
            recommended_movies = data[['Title', 'Director', 'Cast', 'poster_path', 'genres', 'overview']].iloc[movie_indices].copy()
        
        # Format the data for better display
        recommended_movies['Title'] = recommended_movies['Title'].str.title()  # Capitalize movie titles
        recommended_movies['poster_path'] = BASE_POSTER_URL + recommended_movies['poster_path'].fillna('')
        recommended_movies['overview'] = recommended_movies['overview'].fillna('No overview available')
        recommended_movies['Director'] = recommended_movies['Director'].fillna('Unknown')
        recommended_movies['Cast'] = recommended_movies['Cast'].fillna('Unknown')
        recommended_movies['genres'] = recommended_movies['genres'].fillna('Unknown')
        
        return recommended_movies
    except Exception as e:
        print(f"Error during recommendation generation: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """Autocomplete/suggestions API for real-time movie search"""
    query = request.args.get('q', '').strip().lower()
    limit = int(request.args.get('limit', 10))
    
    if not query or len(query) < 2:
        return jsonify([])
    
    try:
        # Get movies that start with the query
        starts_with = data[data['Title'].str.startswith(query, na=False)]
        
        # Limit results
        if len(starts_with) > limit:
            starts_with = starts_with.head(limit)
        
        # Return only titles for autocomplete
        suggestions = starts_with['Title'].str.title().tolist()
        return jsonify(suggestions)
    except Exception as e:
        print(f"Error in autocomplete: {e}")
        return jsonify([])

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'No movie title provided!'}), 400

    title = title.strip()
    results = recommendations(title)
    if results is None or results.empty:
        return jsonify({'error': f"Movie '{title}' not found. Please check the spelling or try searching for it first."})

    # Debugging: Log the recommendations being returned
    print(f"Returning {len(results)} recommendations for '{title}'")
    return jsonify(results.to_dict(orient='records'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'error': 'No search query provided!'}), 400
    
    results = search_movies(query, limit)
    if results is None or results.empty:
        return jsonify({'error': f"No movies found matching '{query}'."})
    
    return jsonify(results.to_dict(orient='records'))

@app.route('/popular', methods=['GET'])
def popular():
    limit = request.args.get('limit', 20, type=int)
    results = get_popular_movies(limit)
    
    if results is None or results.empty:
        return jsonify({'error': 'Unable to fetch popular movies.'})
    
    return jsonify(results.to_dict(orient='records'))

@app.route('/genres', methods=['GET'])
def genres():
    genre_list = get_genres()
    return jsonify(genre_list)

@app.route('/genre/<genre_name>', methods=['GET'])
def movies_by_genre(genre_name):
    limit = request.args.get('limit', 20, type=int)
    results = get_movies_by_genre(genre_name, limit)
    
    if results is None or results.empty:
        return jsonify({'error': f"No movies found for genre '{genre_name}'."})
    
    return jsonify(results.to_dict(orient='records'))

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        if data is None:
            return jsonify({'error': 'Dataset not available'})
        
        stats = {
            'total_movies': len(data),
            'total_genres': len(get_genres()),
            'top_genres': get_top_genres(5),
            'movies_per_decade': get_movies_per_decade(),
            'top_directors': get_top_directors(10),
            'dataset_info': {
                'columns': list(data.columns),
                'sample_size': min(len(data), 1000)
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to get statistics'})

# Helper functions for statistics
def get_top_genres(limit=5):
    try:
        genre_counts = {}
        for genres_str in data['genres'].dropna():
            if isinstance(genres_str, str):
                genres = [g.strip() for g in genres_str.split(',')]
                for genre in genres:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        return sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    except:
        return []

def get_movies_per_decade():
    try:
        # This would require a release_date column, returning dummy data for now
        return {
            '2020s': 150,
            '2010s': 890,
            '2000s': 750,
            '1990s': 650,
            '1980s': 420
        }
    except:
        return {}

def get_top_directors(limit=10):
    try:
        director_counts = data['Director'].value_counts().head(limit)
        return [(director, count) for director, count in director_counts.items()]
    except:
        return []

# SEO Routes - Sitemap and Robots.txt
@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap for search engines"""
    try:
        return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')
    except:
        return "Sitemap not found", 404

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for search engine crawlers"""
    try:
        return send_from_directory('.', 'robots.txt', mimetype='text/plain')
    except:
        return "Robots.txt not found", 404

if __name__ == "__main__":
    app.run(debug=True)
