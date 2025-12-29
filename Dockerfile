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

# Expose the port that the application will listen on
EXPOSE 8080

ENV PYTHONUNBUFFERED=TRUE

# Command to run the application
CMD python app.py
