# Trending Movies Dashboard with Airflow ETL

## Project Overview

This project is a real-time trending movies dashboard that utilizes an ETL (Extract, Transform, Load) pipeline to fetch data from the TMDB API, transform it, and load it into a PostgreSQL database. Built with Streamlit, it provides users with an up-to-date view of trending movies, genres, ratings, and descriptions, with daily updates via an automated Airflow pipeline.

![ETL Pipeline Diagram](Support process example (2).png)

## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [TMDB API](#tmdb-api)
- [Database Management with pgAdmin](#database-management-with-pgadmin)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

- Python
- Streamlit
- PostgreSQL
- Apache Airflow
- TMDB API
- Docker

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lostdir/movie_dashboard_with_airflow_etl.git
   cd movie_dashboard_with_airflow_etl
2. **create a .env file:**
   ```plaintext
    TMDB_API_KEY=your_api_key_here
    AIRFLOW_UID=50000
    DB_HOST=movie_etl_pipline_to_dashboard-postgres-1 #container name 
    DB_PORT=5432
    DB_NAME=ps_db
    DB_USER=airflow
    DB_PASSWORD=airflow
3. **Build and run the Docker containers:**
   ```bash
    docker-compose up --build

