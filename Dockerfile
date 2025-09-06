# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for psycopg
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Copy the start script and make it executable
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Define the command to run your application
CMD ["/bin/bash", "/start.sh"]