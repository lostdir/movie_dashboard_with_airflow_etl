
# Trending Movies Dashboard with Airflow ETL

## Project Overview
This project is a real-time trending movies dashboard that uses a fully automated **ETL (Extract, Transform, Load)** pipeline. The pipeline fetches trending movie data from the **TMDB API**, processes it, and stores it in a **PostgreSQL** database. The dashboard, built using **Streamlit**, provides a real-time interface for users to view updated details such as genres, ratings, and descriptions of trending movies. The data is refreshed daily by an Airflow pipeline running in a Dockerized environment.Users can filter movies based on genres, release year, and minimum ratings, enhancing the overall browsing experience.

![etlflow](https://github.com/user-attachments/assets/3cec7aa3-3f6f-45ea-907c-ec39174cc597)

The pipeline's modular design ensures separation of concerns, with Airflow orchestrating the ETL process, PostgreSQL acting as the persistent data store, and Streamlit providing the user interface.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [TMDB API](#tmdb-api)
- [Database Management with pgAdmin](#database-management-with-pgadmin)
- [Airflow Pipeline and Webserver Connection Setup](#airflow-pipeline-and-webserver-connection-setup)
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
```
2. **Create a .env file:**  
This file will store your environment variables.
```plaintext
TMDB_API_KEY=your_api_key_here
AIRFLOW_UID=50000
DB_HOST=movie_etl_pipline_to_dashboard-postgres-1  # container name of postgres in docker
DB_PORT=5432
DB_NAME=db #database name
DB_USER=airflow
DB_PASSWORD=airflow
```
3. **Build and run the Docker containers:**
```bash
docker-compose up --build
```

## Usage
1. Access **pgAdmin** via `localhost:5050`.
    - Default email: `admin@admin.com`
    - Default password: `root`
2. Visit **Airflow** via `localhost:8080` to view and manage the DAGs (Directed Acyclic Graphs).
    - Use the default username `airflow` and password `airflow`.
3. Visit the **Streamlit app** at `localhost:8501` to interact with the movie dashboard.

## TMDB API
This project retrieves movie data using the **TMDB API**. To use this API, you must sign up and generate an API key on the [TMDB website](https://www.themoviedb.org/). The API key should be placed in the `.env` file under the `TMDB_API_KEY` field.

## Database Management with pgAdmin
- **pgAdmin** is a web-based database management tool for **PostgreSQL**. 
- Once pgAdmin is running (via Docker), you can access it through your browser at `localhost:5050`.
- Use the default login credentials:
    - Email: `admin@admin.com`
    - Password: `root`
- Through pgAdmin, you can explore database schemas, run SQL queries, and monitor the ETL pipeline's data storage.

## Airflow Pipeline and Webserver Connection Setup

### Airflow Pipeline Overview:
The ETL process is managed by **Apache Airflow**, orchestrating the extraction, transformation, and loading of movie data from TMDB into PostgreSQL.

### PostgreSQL Connections in Airflow:

1. **PostgreSQL Connection**:

To configure the **PostgreSQL** connection in Airflow via the **web UI**:

- **Open the Airflow Webserver**:
  - Go to `localhost:8080`.
  - Log in with:
    - Username: `airflow`
    - Password: `airflow`
  
- **Navigate to Admin -> Connections**:
  - In the top menu, click **Admin**.
  - Select **Connections** from the dropdown.

- **Create a New Connection**:
  - Click **+** to add a new connection.

- **Fill in Connection Details**:
  - **Connection Id**: `postgres_conn` #connection name
  - **Connection Type**: `Postgres`
  - **Host**: `postgres`
  - **Database**: `db` #database name for storing  
  - **Login**: `airflow`
  - **Password**: `airflow`
  - **Port**: `5432`

- **Save** the connection. Airflow will now be able to connect to PostgreSQL using this connection ID (`postgres_conn`).


## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch-name`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Open a pull request.

## License
This project is licensed under the [Apache License 2.0](LICENSE).

