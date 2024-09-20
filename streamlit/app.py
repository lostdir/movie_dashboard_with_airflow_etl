import streamlit as st
import pandas as pd
import psycopg2
import os
import requests

# Load environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

TMDB_API_KEY = os.getenv('API_KEY')  # Make sure you add this to .env

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Fetch movie posters using TMDB API
def fetch_poster_path(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url).json()
        poster_path = response['results'][0]['poster_path'] if response['results'] else None
        return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    except:
        return None

# Load movie data
def load_data():
    conn = get_connection()
    query = "SELECT title, genres, vote_average, vote_count, overview, release_date FROM movies"  # Adjusted query
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Fetch posters for movies and add to the DataFrame
    df['poster'] = df['title'].apply(fetch_poster_path)
    
    return df

# Streamlit App
def main():
    st.title('🎬 Trending Movies Today ')

    # Load data from PostgreSQL
    try:
        data = load_data()

        # Remove any unwanted columns
        data.dropna(subset=['title', 'genres'], inplace=True)

        # Create a user-friendly layout
        for i, row in data.iterrows():
            col1, col2 = st.columns([1, 3])  # Two-column layout: one for the poster, one for details
            
            with col1:
                # Display movie poster
                if row['poster']:
                    st.image(row['poster'], use_column_width=True)
                else:
                    st.image('https://via.placeholder.com/150', use_column_width=True)  # Placeholder image if poster is missing

            with col2:
                # Display movie details
                st.subheader(row['title'])
                st.write(f"**Genre:** {row['genres']}")
                st.write(f"**Rating:** ⭐ {row['vote_average']}")
                st.write(f"**Vote Count:** {row['vote_count']}")
                st.write(f"**Description:** {row['overview']}")
                st.write(f"**Release Date:** {row['release_date']}")
                

            st.markdown("---")  # Separator line between movies

    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
