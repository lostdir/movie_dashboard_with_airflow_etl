import requests
import os

# Load environment variables from .env if required
from dotenv import load_dotenv
# Set your  'api_key' with your actual TMDB API key into .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Fetch genre list from TMDB API

def fetch_genres(api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        # Create a dictionary to map genre IDs to genre names
        genre_dict = {genre['id']: genre['name'] for genre in genres}
        return genre_dict
    else:
        raise Exception(f"Error fetching genres from TMDB API. Status code: {response.status_code}")

# Fetch trending movies from TMDB API
def fetch_trending_movies(api_key):
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        raise Exception(f"Error fetching data from TMDB API. Status code: {response.status_code}")

# Print trending movies with genre names
def print_movies(movies, genre_dict):
    for movie in movies:
        title = movie.get('title', 'No title')
        genre_ids = movie.get('genre_ids', [])
        genres = ', '.join([genre_dict.get(genre_id, 'Unknown') for genre_id in genre_ids])
        rating = movie.get('vote_average', 'No rating')
        description = movie.get('overview', 'No description')
        print(f"Title: {title}")
        print(f"Genres: {genres}")
        print(f"Rating: {rating}")
        print(f"Description: {description}")
        print('-' * 40)

if __name__ == "__main__":
    try:
        # Fetch genres and trending movies
        genre_dict = fetch_genres(API_KEY)
        trending_movies = fetch_trending_movies(API_KEY)
        
        # Print the movies with genre names
        print_movies(trending_movies, genre_dict)
    except Exception as e:
        print(f"An error occurred: {e}")
