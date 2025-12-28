# Use the official Python image as the base image
FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

# Set the working directory inside the container
WORKDIR /app

# Install other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN pip install --no-cache-dir playwright
RUN playwright install --with-deps

# Copy the application code into the container
COPY . .

# Expose the port that Gunicorn will listen on
EXPOSE 8080

ENV PYTHONUNBUFFERED=TRUE

# Command to run the application using Uvicorn
CMD uvicorn app:app --host 0.0.0.0 --port 8080 --workers 2 --timeout-keep-alive 3600
# CMD python scrape.py
