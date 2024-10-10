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
    query = "SELECT title, genres, vote_average, vote_count, overview, release_date FROM movies"
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert release_date to datetime and format it
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.date  # Only keep the date part
    df['release_year'] = df['release_date'].apply(lambda x: x.year if pd.notnull(x) else None)  # Create a new column for the release year
    
    # Fetch posters for movies and add to the DataFrame
    df['poster'] = df['title'].apply(fetch_poster_path)

    return df

# Streamlit App
def main():
    # Set page configuration
    st.set_page_config(page_title="Trending Movies Today", layout="centered")

    # Custom CSS for dark theme styling
    st.markdown(
        """
        <style>
        .main {
            background-color: #121212;  /* Dark background */
            padding: 20px; /* Padding around the app */
        }
        h1 {
            text-align: center; /* Center the title */
            color: #ffffff; /* White for title */
            font-size: 48px; /* Larger font size */
            margin-bottom: 20px; /* Space below the title */
            font-family: 'Arial', sans-serif; /* Font family */
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7); /* Shadow effect */
        }
        .stButton>button {
            background-color: #1db954; /* Green button color */
            color: white; /* Button text color */
        }
        .stSelectbox>div>div {
            background-color: #1e1e1e; /* Darker background for dropdowns */
            color: #ffffff; /* White text for dropdown */
        }
        .stSelectbox>div>label {
            color: #ffffff; /* White label for dropdowns */
        }
        .stMarkdown, .stWrite {
            color: #ffffff; /* White text for descriptions */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1>🎬 Trending Movies Today</h1>", unsafe_allow_html=True)  # Use HTML for the title

    # Load data from PostgreSQL
    try:
        data = load_data()

        # Remove any unwanted columns
        data.dropna(subset=['title', 'genres'], inplace=True)

        # --- Filter Options ---
        col1, col2, col3 = st.columns(3)

        # Genre filter (show unique genres)
        with col1:
            unique_genres = set()
            for genre_list in data['genres']:
                unique_genres.update(genre_list.split(", "))  # Assuming genres are comma-separated
            genre_options = sorted(unique_genres)
            genre_options.insert(0, 'All')  # Add 'All' as the first option
            selected_genre = st.selectbox('Select Genre', genre_options)

        # Release Year filter
        with col2:
            release_years = sorted(data['release_year'].unique())
            selected_year = st.selectbox('Select Release Year', ['All'] + list(release_years))

        # Rating filter (1 to 10)
        with col3:
            rating_options = list(range(1, 11))  # Create a list from 1 to 10
            selected_rating = st.selectbox('Select Minimum Rating', ['All'] + rating_options)

        # Check if no filters are selected
        if selected_genre == 'All' and selected_year == 'All' and selected_rating == 'All':
            filtered_data = data  # No filters, display all data
        else:
            # Apply filters to the DataFrame
            filtered_data = data[
                ((data['genres'].str.contains(selected_genre)) if selected_genre != 'All' else True) &
                ((data['release_year'] == int(selected_year)) if selected_year != 'All' else True) &
                ((data['vote_average'] >= selected_rating) if selected_rating != 'All' else True)
            ]

        # Display filtered results
        st.write(f"Showing {len(filtered_data)} results:")

        # Create a user-friendly layout
        for i, row in filtered_data.iterrows():
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
