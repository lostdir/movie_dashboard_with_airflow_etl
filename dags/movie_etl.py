import os
from datetime import datetime, timedelta
from airflow import DAG
import requests
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from dotenv import load_dotenv


load_dotenv()

# Fetch API key from environment variable
API_KEY = os.getenv('API_KEY')

# Fetch genre list from TMDB API
def fetch_genres(**kwargs):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        genres = response.json().get('genres', [])
        # Create a dictionary to map genre IDs to genre names
        genre_dict = {genre['id']: genre['name'] for genre in genres}
        # Push the genre_dict to XCom for later tasks
        kwargs['ti'].xcom_push(key='genre_dict', value=genre_dict)
    else:
        raise Exception(f"Error fetching genres from TMDB API. Status code: {response.status_code}")

# Fetch trending movies from TMDB API
def fetch_trending_movies(**kwargs):
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        trending_movies = response.json()['results']
        # Push trending movies to XCom for later tasks
        kwargs['ti'].xcom_push(key='trending_movies', value=trending_movies)
    else:
        raise Exception(f"Error fetching data from TMDB API. Status code: {response.status_code}")

# Store movies in PostgreSQL using PostgresHook
def store_in_postgres(**kwargs):
    ti = kwargs['ti']
    trending_movies = ti.xcom_pull(task_ids='fetch_trending_movies', key='trending_movies')
    genre_dict = ti.xcom_pull(task_ids='fetch_genres', key='genre_dict')

    if not trending_movies:
        raise Exception("No trending movies found in XCom.")
    
    if not genre_dict:
        raise Exception("No genre dictionary found in XCom.")

    pg_hook = PostgresHook(postgres_conn_id='movie_conn')

    # Delete old data from the table
    pg_hook.run("DELETE FROM movies;")

    for rank, movie in enumerate(trending_movies, start=1):
        movie_id = movie['id']
        title = movie['title']
        overview = movie['overview']
        release_date = movie['release_date']
        vote_average = movie['vote_average']
        vote_count = movie['vote_count']

        genre_ids = movie['genre_ids']
        genres = ', '.join([genre_dict.get(str(genre_id), 'Unknown') for genre_id in genre_ids])

        INSERT_MOVIES_SQL = """
            INSERT INTO movies (id, title, overview, release_date, vote_average, vote_count, genres, rank)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET title = EXCLUDED.title,
                overview = EXCLUDED.overview,
                release_date = EXCLUDED.release_date,
                vote_average = EXCLUDED.vote_average,
                vote_count = EXCLUDED.vote_count,
                genres = EXCLUDED.genres,
                rank = EXCLUDED.rank;
        """
        pg_hook.run(INSERT_MOVIES_SQL, parameters=(movie_id, title, overview, release_date, vote_average, vote_count, genres, rank))




# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'trending_movies_dag',
    default_args=default_args,
    description='DAG to create table, fetch trending movies, and store them in PostgreSQL',
    schedule_interval=timedelta(days=1),
)

# Task 1: Create table
create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='movie_conn',
    sql=""" 
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        rank INTEGER,
        title VARCHAR(255),
        overview TEXT,
        release_date DATE,
        vote_average FLOAT,
        vote_count INTEGER,
        genres TEXT
    );
    """,
    dag=dag,
)

# Task 2: Fetch genres
fetch_genres_task = PythonOperator(
    task_id='fetch_genres',
    python_callable=fetch_genres,
    dag=dag,
)

# Task 3: Fetch trending movies
fetch_trending_movies_task = PythonOperator(
    task_id='fetch_trending_movies',
    python_callable=fetch_trending_movies,
    dag=dag,
)

# Task 4: Store movies in PostgreSQL
store_movies_in_postgres_task = PythonOperator(
    task_id='store_movies_in_postgres',
    python_callable=store_in_postgres,
    dag=dag,
)

# Set dependencies
create_table_task >> fetch_genres_task >> fetch_trending_movies_task >> store_movies_in_postgres_task
