# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Python server script into the container
COPY server.py .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install psycopg2-binary \
    && rm -rf /var/lib/apt/lists/*

# Expose the port that your Python server will run on
EXPOSE 8000

# Run the Python server
CMD ["python", "./server.py"]