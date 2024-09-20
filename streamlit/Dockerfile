FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files to the container
COPY . /app

# Install dependencies (use psycopg2-binary instead of psycopg2)
RUN pip install --upgrade pip && \
    pip install streamlit psycopg2-binary pandas python-dotenv
RUN pip install python-dotenv


# Expose Streamlit's default port
EXPOSE 8501

# Run the streamlit app
CMD ["streamlit", "run", "app.py"]
